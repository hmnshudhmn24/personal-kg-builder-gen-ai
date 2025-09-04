# streamlit_app.py
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()
st.set_page_config(page_title="Personal KG Builder — gen-ai", layout="wide")
st.title("🧠 Personal Knowledge Graph Builder — gen-ai")

from src.ingest import ingest_text, ingest_pdf_bytes
from src.graph_query import nl_query_to_cypher, run_cypher_query_and_summarize
from src.neo4j_client import get_stats, export_recent_subgraph_image

st.sidebar.header("Neo4j")
if st.sidebar.button("Show DB stats"):
    st.sidebar.json(get_stats())

st.header("1) Ingest notes / bookmarks / chats")
with st.expander("Ingest"):
    text_input = st.text_area("Paste or type notes / bookmarks / chat logs", height=240)
    uploaded_pdf = st.file_uploader("Or upload a small PDF", type=["pdf"])
    source_label = st.text_input("Source label (optional)", value="notes")
    chunk_size = st.number_input("Chunk size", value=int(os.getenv('CHUNK_SIZE', 500)))
    overlap = st.number_input("Chunk overlap", value=int(os.getenv('CHUNK_OVERLAP', 50)))
    if st.button("Ingest"):
        if uploaded_pdf is not None:
            data = uploaded_pdf.read()
            n = ingest_pdf_bytes(data, source=uploaded_pdf.name, chunk_size=chunk_size, overlap=overlap)
            st.success(f"Ingested PDF into {n} chunks.")
        elif text_input.strip():
            n = ingest_text(text_input, source=source_label, chunk_size=chunk_size, overlap=overlap)
            st.success(f"Ingested text into {n} chunks.")
        else:
            st.warning("Paste text or upload PDF to ingest.")

st.write('---')
st.header('2) Query your graph in natural language')
query = st.text_input("Ask a question (e.g., 'What did I note about transformer models?')")
safe_mode = st.checkbox("Confirm generated Cypher before executing", value=True)
top_k = st.number_input("Top-k chunks for semantic fallback", value=5, min_value=1, max_value=20)

if st.button("Run query") and query.strip():
    suggestion = nl_query_to_cypher(query, top_k=top_k)
    st.subheader("Suggested Cypher")
    st.code(suggestion.get('cypher', '-- no cypher --'))
    st.write("LLM explanation:")
    st.write(suggestion.get('explanation', ''))
    if safe_mode:
        if st.button("Execute suggested Cypher"):
            res = run_cypher_query_and_summarize(suggestion.get('cypher',''), query)
            st.subheader("Answer / Summary")
            st.write(res.get('answer',''))
            if res.get('rows'):
                st.table(res['rows'])
    else:
        res = run_cypher_query_and_summarize(suggestion.get('cypher',''), query)
        st.subheader("Answer / Summary")
        st.write(res.get('answer',''))
        if res.get('rows'):
            st.table(res['rows'])

st.write('---')
st.header('3) Small graph preview')
if st.button("Show recent subgraph"):
    p = export_recent_subgraph_image(limit=40)
    if p:
        st.image(p, use_column_width=True)
    else:
        st.info("No graph data yet. Ingest some notes first.")
