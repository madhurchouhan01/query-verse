# __import__('pysqlite3')
# import sys
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from pydantic import BaseModel

from crewai.flow import Flow, listen, start, router

from crews.poem_crew.poem_crew import QueryCrew, QueryGenCrew, IDUGenCrew, GeneralQA, MainAgent
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Define the state model
class QueryState(BaseModel):
    query: str = ""
    history: list = []
    sql_query: str = ""
    final_response: str = ""

# Define the flow using CrewAI
class QueryFlow(Flow[QueryState]):

    @start()
    def main(self):
        result = MainAgent().crew().kickoff(       
                inputs={
                    "query": self.state.query,
                    "history": self.state.history
                })
        self.state.final_response = result.raw
        return result.raw

    @router(main)
    def routing_func(self):
        print("its calling...📞")
        if 'db' in self.state.final_response.lower():
            return "generate_query_router"
        elif 'qa' in self.state.final_response.lower():
            return "general_qna_router"
        else:
            return 'Invalid Query'

    @listen("general_qna_router")
    def general_qna(self):
        print("its been executed 🔴")
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
            print(f"Error Occured while Generating SQL Query : {e}")
            return f"Error Occured while Generating SQL Query : {e}"

    @router(generate_query)
    def route_query(self):
        try:
            if 'SELECT' in self.state.sql_query.upper():
                return "SELECT"
            elif any(x in self.state.sql_query.upper() for x in ['INSERT', 'DELETE', 'UPDATE']):
                return "IDU"
        except Exception as e:
            print(f"Error Occured while Routing : {e}")
            return f"Error Occured while Routing : {e}"

    @listen("SELECT")
    def select_query(self):
        try:
            result = QueryGenCrew().crew().kickoff(inputs={"sql_query": self.state.sql_query})
            self.state.final_response = result.raw
            self.state.history.append(f"AI: {self.state.final_response}")
            return "end"
        except Exception as e:
            print(f"Error Occured while Executing SELECT Query : {e}")
            return f"Error Occured while Executing SELECT Query : {e}"

    @listen("IDU")
    def idu_query(self):
        try:
            result = IDUGenCrew().crew().kickoff(inputs={"sql_query": self.state.sql_query})
            self.state.final_response = result.raw
            self.state.history.append(f"AI: {self.state.final_response}")
            return "end"
        except Exception as e:
            print(f"Error Occured while Executing IDU Query : {e}")
            return f"Error Occured while Executing IDU Query : {e}"

    @listen('end')
    def end_func(self):
        return self.state.final_response
    
# --- Streamlit UI Setup ---
st.set_page_config(page_title="SQL Query Assistant", layout="centered")
st.title("🧠 SQL Query Assistant")

# Initialize session state objects if they don't exist.
if "query_state" not in st.session_state:
    st.session_state.query_state = QueryState()
if "messages" not in st.session_state:
    st.session_state.messages = []  # To hold chat messages as {"role": "user"/"assistant", "content": "..."}

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input: using st.chat_input for a conversational interface.
if user_input := st.chat_input("Type your query here..."):
    # Add user message to the chat history.
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Update the QueryState from the input.
    st.session_state.query_state.query = user_input 
    st.session_state.query_state.history.append(f"User: {user_input}")
    
    # Instantiate the flow and update its internal state from session_state.
    query_flow = QueryFlow()
    query_flow.state.query = st.session_state.query_state.query
    query_flow.state.history = st.session_state.query_state.history
    with st.spinner("Processing Your Input..."):
        # Kick off the flow; note that kickoff() only accepts the inputs dictionary.
        response = query_flow.kickoff(inputs={"query": user_input})
    
    # Update the session state's query object from the flow state (to persist any changes).
    st.session_state.query_state = query_flow.state

    # Append and display the AI response.
    st.session_state.messages.append({"role": "assistant", "content": st.session_state.query_state.final_response})
    with st.chat_message("assistant"):
        st.markdown(st.session_state.query_state.final_response)
