# 🧠🔗 Personal Knowledge Graph Builder (Gen-AI)

Turn your **notes, chats, and bookmarks** into an interactive **knowledge graph** you can **query in natural language**.  
Powered by **Neo4j**, **embeddings**, and **LLMs** — so you can visually explore and reason over your own information.



## 🚀 Why?

> In the age of information overload, our ideas live scattered in files, chats, and links.  
> This tool **connects the dots**, helping you **discover insights** you didn’t even know you had.



## ✨ Features

- 📥 **Ingest Notes & Files** – Drop Markdown, text, or snippets for instant indexing  
- 🧬 **Embeddings + Graph** – Create **semantic nodes & relationships**  
- 🗣️ **Natural Language Query** – Ask questions, get Cypher-backed answers  
- 🌐 **Neo4j Visualization** – Explore your graph with a beautiful UI  
- ⚙️ **Modular Code** – Swap in any embedding or LLM provider easily  
- 🔐 **Private by Design** – Your knowledge graph stays **local-first**



## 🛠️ Tech Stack

- **Neo4j** – Graph database & visualization  
- **OpenAI / LLM** – Embeddings & Cypher query generation  
- **Streamlit** – Lightweight UI  
- **Python** – Data ingestion, parsing, and glue logic



## 📂 Project Structure

```
personal-kg-builder-gen-ai/
│── .env.example          # API keys & config
│── requirements.txt      # Dependencies
│── README.md             # Documentation
│── streamlit_app.py      # UI for ingestion & querying
└── src/
    ├── __init__.py
    ├── config.py         # Env settings, constants
    ├── neo4j_client.py   # Connect, create nodes, relationships
    ├── embeddings.py     # Wrapper for OpenAI embeddings
    ├── ingest.py         # Load notes/files, create graph entities
    ├── graph_query.py    # NL query → Cypher → Graph result
    └── utils.py          # Helpers (text cleaning, I/O)
```



## ⚡ Quickstart

### 1️⃣ Clone & Setup
```bash
git clone https://github.com/your-username/personal-kg-builder-gen-ai.git
cd personal-kg-builder-gen-ai
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2️⃣ Configure
- Copy `.env.example` → `.env`
- Add your keys:
```
OPENAI_API_KEY=sk-xxxx
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
```

### 3️⃣ Run Neo4j
```bash
docker run -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/your_password neo4j:5.20
```

### 4️⃣ Launch the App
```bash
streamlit run streamlit_app.py
```



## 🎯 How It Works

1. **Ingestion:** Upload text/Markdown or paste notes → embeddings created → nodes & relationships stored in Neo4j.  
2. **Query:** Type a natural language question → LLM generates Cypher → executes against Neo4j → results returned.  
3. **Explore:** Use Neo4j Browser or Streamlit graph panel to visualize connections.



## 📊 Example Query

> Prompt: *"Show me all notes related to 'quantum computing' and their connected topics."*  
> Response: Graph nodes highlighting all your notes mentioning **quantum computing** and links to related concepts.



## 🔮 Roadmap

- [ ] Support **PDF & web clipper** ingestion  
- [ ] Add **contextual Q&A** (RAG) over graph nodes  
- [ ] Fine-tune **embedding model** for personal domain knowledge  
- [ ] Add **offline mode** with local LLMs


