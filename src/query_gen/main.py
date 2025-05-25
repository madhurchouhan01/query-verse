from pydantic import BaseModel
from crewai.flow import Flow, listen, start, router
from crews.poem_crew.poem_crew import QueryCrew, QueryGenCrew, IDUGenCrew, GeneralQA, MainAgent
import streamlit as st
from dotenv import load_dotenv
import time

load_dotenv()

# Define the state model
class QueryState(BaseModel):
    query: str = ""
    history: list = []
    sql_query: str = ""
    final_response: str = ""
    query_type : str = ""

# Define the flow using CrewAI
class QueryFlow(Flow[QueryState]):

    @start()
    def main(self):
        result = MainAgent().crew().kickoff(       
                inputs={
                    "query": self.state.query,
                    "history": self.state.history
                })
        self.state.query_type = result.raw
        return result.raw

    @router(main)
    def routing_func(self):
        if 'db' in self.state.query_type.lower():
            return "generate_query_router"
        elif 'qa' in self.state.query_type.lower():
            return "general_qna_router"
        else:
            return 'Invalid Query'

    @listen("general_qna_router")
    def general_qna(self):
        try:
            result = GeneralQA().crew().kickoff(       
                inputs={
                    "query": self.state.query,
                    "history": self.state.history
                })
            
            self.state.final_response = result.raw
            return "end"
        except Exception as e:
            return f"Error occured while Q and A execution : {e}"

    @listen("generate_query_router")
    def generate_query(self):
        try:
            result = QueryCrew().crew().kickoff(
                inputs={
                    "query": self.state.query,
                    "history": self.state.history
                }
            )
            self.state.sql_query = result.raw
            return self.state.sql_query
        except Exception as e:
            return f"Error Occured while Generating SQL Query : {e}"

    @router(generate_query)
    def route_query(self):
        try:
            if any(x in self.state.sql_query.upper() for x in['SELECT', 'SHOW', 'DESCRIBE ']):
                return "DDL"
            elif any(x in self.state.sql_query.upper() for x in ['INSERT', 'DELETE', 'UPDATE', 'MERGE','CREATE','ALTER','DROP','TRUNCATE','RENAME', ]):
                return "DML"
        except Exception as e:
            return f"Error Occured while Routing : {e}"

    @listen("DDL")
    def select_query(self):
        try:
            result = QueryGenCrew().crew().kickoff(inputs={"sql_query": self.state.sql_query})
            self.state.final_response = result.raw
            self.state.history.append(f"AI: {self.state.final_response}")
            return "end"
        except Exception as e:
            return f"Error Occured while Executing SELECT Query : {e}"

    @listen("DML")
    def idu_query(self):
        try:
            result = IDUGenCrew().crew().kickoff(inputs={"sql_query": self.state.sql_query})
            self.state.final_response = result.raw
            self.state.history.append(f"AI: {self.state.final_response}")
            return "end"
        except Exception as e:
            return f"Error Occured while Executing IDU Query : {e}"

    @listen('end')
    def end_func(self):
        return self.state.final_response

# Custom CSS for beautiful styling
def load_custom_css():
    st.markdown("""
    <style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Send+Flowers&family=Tangerine:wght@400;700&display=swap');
    
    /* Global styles */
    .stApp {
        background: linear-gradient(90deg,rgba(217, 217, 217, 1) 0%, rgba(199, 199, 255, 1) 45%, rgba(191, 243, 255, 1) 100%);
        font-family: 'Inter', sans-serif;
    }
    body {
        background: linear-gradient(90deg,rgba(217, 217, 217, 1) 0%, rgba(199, 199, 255, 1) 45%, rgba(191, 243, 255, 1) 100%)
        background-attachment: fixed;
    }
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        margin-bottom: 2rem;
        border: 1px solid rgba(0, 0, 0, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .main-title {
        font-family: "Send Flowers", cursive;
        font-weight: 700;   
        font-size: 3rem;
        background: linear-gradient(135deg, #fff 0%, #f0f8ff 100%);
        -webkit-background-clip: text;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .main-subtitle {
        font-size: 1.2rem;
        color: rgba(0, 0, 0, 0.8);
        font-weight: 400;
    }
    
    /* Chat container */
    .chat-container {
        background: rgba(0, 0, 0, 0.95);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 0, 0, 0.3);
    }
    div[class^="st-emotion-cache-uhkwx6"] {
        background: linear-gradient(90deg,rgba(217, 217, 217, 1) 0%, rgba(199, 199, 255, 1) 45%, rgba(191, 243, 255, 1) 100%);
        color: black !important;
        border-radius: 15px;
        padding: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    }
                
    /* Message styling */
    .stChatMessage {
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease;
    }
    
    .stChatMessage:hover {
        transform: translateY(-2px);
    }
    
    /* User message */
    .stChatMessage[data-testid="user-message"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: black;
        margin-left: 20%;
    }
    
    /* Assistant message */
    .stChatMessage[data-testid="assistant-message"] {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: black;
        margin-right: 20%;
    }
    
    /* Input styling */
    /* Enhanced Chat Input Styling */
    .stChatInput > div {
        background: white;
    
        border: 2px solid rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(12px) saturate(120%);
        -webkit-backdrop-filter: blur(12px) saturate(120%);
        box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.05),
                    0 4px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        padding: 12px 16px;
        color: #ffffff;
        font-size: 4rem;
    }

    /* Focused State */
    .stChatInput > div:focus-within {
        border-color: #8a7eea;
        box-shadow: 0 0 10px rgba(138, 126, 234, 0.6),
                    0 0 25px rgba(138, 126, 234, 0.2);
        transform: translateY(-2px);
    }

    
    /* Spinner customization */
    .stSpinner {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }
    
    /* Stats cards */
    .stats-container {
        display: flex;
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .stat-card {
        background: rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(0, 0, 0, 0.2);
        flex: 1;
        transition: transform 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: black;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        color: rgba(0, 0, 0, 0.8);
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
        backdrop-filter: blur(10px);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: black;
        border: none;
        border-radius: 25px;
        padding: 0.7rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if "query_state" not in st.session_state:
        st.session_state.query_state = QueryState()
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "total_queries" not in st.session_state:
        st.session_state.total_queries = 0
    if "db_queries" not in st.session_state:
        st.session_state.db_queries = 0
    if "qa_queries" not in st.session_state:
        st.session_state.qa_queries = 0

# Display stats
def display_stats():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{st.session_state.total_queries}</div>
            <div class="stat-label">Total Queries</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{st.session_state.db_queries}</div>
            <div class="stat-label">Database Queries</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{st.session_state.qa_queries}</div>
            <div class="stat-label">Q&A Queries</div>
        </div>
        """, unsafe_allow_html=True)

# Typing animation effect
def typing_animation(text, placeholder):
    displayed_text = ""
    for char in text:
        displayed_text += char
        placeholder.markdown(f"🤖 {displayed_text}▌")
        time.sleep(0.02)
    placeholder.markdown(f"🤖 {text}")

# Main app
def main():
    # Page config
    st.set_page_config(
        page_title="Query Verse - AI Chatbot",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Load custom CSS
    load_custom_css()
    
    # Initialize session state
    init_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <div class="main-title">🧠 Query Verse</div>
        <div class="main-subtitle">Your Intelligent AI Assistant for Database Queries & Q&A</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats section
    display_stats()
    
    # Main chat interface
    # st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    st.markdown('---')
    # Display welcome message if no messages
    if not st.session_state.messages:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown("""
            👋 **Welcome to Query Verse!** 
            
            I'm your intelligent AI assistant, ready to help you with:
            - 🗄️ **Database Queries** - Generate and execute SQL queries
            - ❓ **General Q&A** - Answer questions and provide information
            
            Just type your question below and I'll route it to the right specialist!
            """)
    
    # Display chat history
    for i, msg in enumerate(st.session_state.messages):
        avatar = "👤" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    if user_input := st.chat_input("💬 Ask me anything about databases or general questions..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)
        
        # Update query state
        st.session_state.query_state.query = user_input 
        st.session_state.query_state.history.append(f"User: {user_input}")
        st.session_state.total_queries += 1
        
        # Process query
        query_flow = QueryFlow()
        query_flow.state.query = st.session_state.query_state.query
        query_flow.state.history = st.session_state.query_state.history
        
        # Show processing with beautiful spinner
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("🔮 Processing your query..."):
                response = query_flow.kickoff(inputs={"query": user_input})
            
            # Update session state
            st.session_state.query_state = query_flow.state
            
            # Update stats based on response type
            if 'db' in query_flow.state.query_type.lower():
                st.session_state.db_queries += 1
            elif 'qa' in query_flow.state.query_type.lower():
                st.session_state.qa_queries += 1
            
            # Display response with typing effect
            st.markdown(st.session_state.query_state.final_response)
        
        # Add assistant response to messages
        st.session_state.messages.append({
            "role": "assistant", 
            "content": st.session_state.query_state.final_response
        })
        
        # Rerun to update the interface
        st.rerun()
    
    # Sidebar with additional features
    with st.sidebar:
        st.markdown("### 🎛️ Control Panel")
        
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.session_state.query_state = QueryState()
            st.rerun()
        
        if st.button("📊 Reset Statistics", use_container_width=True):
            st.session_state.total_queries = 0
            st.session_state.db_queries = 0
            st.session_state.qa_queries = 0
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 🚀 Features")
        st.markdown("""
        - **Smart Routing**: Automatically directs queries to appropriate handlers
        - **Database Operations**: Supports SELECT, INSERT, UPDATE, DELETE queries
        - **General Q&A**: Handles knowledge-based questions
        - **Beautiful UI**: Modern glassmorphism design
        - **Real-time Stats**: Track your query patterns
        """)
        
        st.markdown("---")
        st.markdown("### 💡 Tips")
        st.markdown("""
        - Use keywords like 'database', 'select', 'insert' for DB queries
        - Ask general questions for Q&A mode
        - Check the stats to see your usage patterns
        """)

if __name__ == "__main__":
    main()