# 🧠 Personal Knowledge Graph Builder — gen-ai

Build a personal, queryable **Knowledge Graph** from your notes, bookmarks, chats, and PDFs.  
This starter toolkit ingests text, creates semantic embeddings, stores text chunks as nodes in **Neo4j**, links semantically-similar chunks, and lets you query your graph with **natural language** (LLM translates to Cypher or a semantic retrieval fallback).

## Key Features
- 📝 Ingest plain text or PDFs, chunk and embed content.
- 🔗 Create `Chunk` nodes and semantic `SIMILAR_TO` relationships in Neo4j.
- 🧭 Ask questions in plain English — LLM converts to Cypher (safe-mode) or fallback retrieval returns top chunks and an LLM summary.
- 🖼️ Visualize a small subgraph preview.
- 🔁 Modular design: swap OpenAI for local embeddings (sentence-transformers) as needed.

## Quick Start (local)
1. Clone the repo and enter directory
   ```bash
   git clone https://github.com/yourname/personal-kg-builder-gen-ai.git
   cd personal-kg-builder-gen-ai
   ```
2. Create virtual env and install
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
   pip install -r requirements.txt
   ```
3. Start Neo4j (Docker quickstart)
   ```bash
   docker run --rm -p7474:7474 -p7687:7687 -e NEO4J_AUTH=neo4j/changeit neo4j:5
   ```
4. Copy `.env.example` to `.env` and edit credentials & API keys
   ```bash
   cp .env.example .env
   ```
5. Run the Streamlit app
   ```bash
   streamlit run streamlit_app.py
   ```

## Files & Structure
```
personal-kg-builder-gen-ai/
│── .env.example
│── requirements.txt
│── README.md
│── streamlit_app.py
└── src/
    ├── __init__.py
    ├── config.py
    ├── neo4j_client.py      # Neo4j helper (connect, create nodes/rels, query)
    ├── embeddings.py        # embeddings wrapper (OpenAI + local fallback)
    ├── ingest.py           # ingest notes/files/text -> nodes + relationships
    ├── graph_query.py      # natural language -> cypher + RAG query
    └── utils.py            # helpers (text normalization, file reading)
```

## Caveats & Ethics
- This is a research/experimental tool — **not production-ready**.
- Be careful with private or sensitive data; secure your Neo4j instance.
- When using LLMs, costs and privacy apply — you may prefer a local embedding model.

## Roadmap / Improvements
- Add fine-grained entity extraction (NER) and typed relations.
- Use a production vector index (FAISS/HNSW) or Neo4j vector plugin for performance.
- Add authentication and encrypted storage for private notes.
- Add scheduled ingestion (watch folders, RSS, email notes).

---
MIT License © 2025
