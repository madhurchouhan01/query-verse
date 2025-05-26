# 🚀 QueryVerse

> ⚡ An Agentic AI-Powered Natural Language to SQL Interface  
> 🎯 Powered by LLMs, Tracked with AgentOps, Hosted on Railway  
> 💡 [Live Demo](https://query-verse-1.onrender.com)
> 
---

## 🧠 What is QueryVerse?

**QueryVerse** is an AI-first platform that transforms how humans interact with databases. Instead of writing SQL, users simply ask questions in **natural language**, and QueryVerse:

1. **Parses the request** using LLMs
2. **Translates it** into a valid **MySQL** query
3. **Executes the query** on a live **Railway-hosted** database
4. **Returns the results** back in **human-readable natural language**

This project is **integrated with [AgentOps](https://www.agentops.ai/)** to enable intelligent observability and instrumentation of the agentic workflow.

---

## 🔥 Key Features

- 🧠 **Agentic AI Core**: Orchestrated with LLMs and CrewAI for agent-based reasoning
- 📊 **MySQL Compatible**: Query execution runs against live Railway-managed MySQL databases
- 💬 **Natural Language Interface**: No more SQL headaches—just ask what you need
- 📈 **AgentOps Integration**: Full session tracking, telemetry, and performance monitoring
- 🛠️ **Modular and Scalable**: Built to scale across teams and use cases

---

## 🧪 Example Query Flow

> 🧑‍💼 *"Show me all employees in sales department."*  
> ⬇️  
> 🧠 **[LLM Agent]** ➜ `SELECT * FROM employees WHERE dept_name = 'sales';`  
> ⬇️  
> 📦 **[Execution Engine]** ➜ Returns matching records  
> ⬇️  
> 💬 *"Here are employees in sales department..."*

---

## 🛠️ Tech Stack

| Component         | Technology                                    |
|-------------------|-----------------------------------------------|
| 🤖 Agent Runtime  | [CrewAI](https://crewai.dev)                |
| 🧠 LLM Backend    | [Groq](https://groq.com)                    |
| 📦 Database       | MySQL on [Railway](https://railway.app)     |
| 📊 Monitoring     | [AgentOps](https://agentops.ai)             |
| 🖥️ Frontend       | [Streamlit](https://streamlit.io)           |

---

## 🧰 Installation

```bash
# Clone the repository
git clone https://github.com/madhurchouhan01/query-verse.git
cd query-verse

# Sync CrewAI virtual environment
uv sync

# Create and activate a virtual environment
python -m venv .venv
source .venv/Scripts/activate  # On Windows
# source .venv/bin/activate    # On macOS/Linux

# Install dependencies
uv pip install -r requirements.txt

# Navigate to main file
cd src/query_gen/

# Run Streamlit UI
streamlit run main.py
```

> ⚠️ **Don't forget to create MySQL database using file `backup.sql`**  
> ⚙️ Add a **.env** file to store the API Keys

---

## 🌐 Deployment

### Coming Soon 🚧

We're working on deploying QueryVerse with a web UI, featuring:

- ✨ **Drag-and-drop** DB uploads
- 🎯 **Interactive** query suggestions  
- 🔄 **Streaming** LLM responses

*Stay tuned.*

---

## 🧠 Future Roadmap

- [ ] 🔐 User authentication and access control
- [ ] 📁 Database upload + schema preview
- [ ] 🌍 Multi-database support (PostgreSQL, SQLite)
- [ ] 📊 Advanced analytics and query optimization

---

## 🤝 Contributing

**We move fast and break things—with precision.**

- 🌟 **Star us** if you find this useful
- 🍴 **Fork us** to contribute
- 📥 **PRs welcome** - let's build together
- 🐛 **Issues** help us improve

### Development Setup

```bash
# Fork the repo and clone your fork
git clone https://github.com/YOUR_USERNAME/query-verse.git

# Create a feature branch
git checkout -b feature/amazing-feature

# Make your changes and commit
git commit -m "Add amazing feature"

# Push to your fork and create a PR
git push origin feature/amazing-feature
```

---


## 🙏 Acknowledgments

- [CrewAI](https://crewai.dev) for the agentic framework
- [AgentOps](https://agentops.ai) for observability
- [Railway](https://railway.app) for seamless database hosting
- [Groq](https://groq.com) for lightning-fast LLM inference

---

<div align="center">

**Built with ❤️, LLMs, and a healthy disrespect for old-school SQL interfaces.**

[![GitHub stars](https://img.shields.io/github/stars/madhurchouhan01/query-verse?style=social)](https://github.com/madhurchouhan01/query-verse/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/madhurchouhan01/query-verse?style=social)](https://github.com/madhurchouhan01/query-verse/network/members)
[![GitHub issues](https://img.shields.io/github/issues/madhurchouhan01/query-verse)](https://github.com/madhurchouhan01/query-verse/issues)

</div>
