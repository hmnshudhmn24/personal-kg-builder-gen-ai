# src/ingest.py
from .utils import chunk_text, extract_text_from_pdf_bytes, clean_text
from .embeddings import embed_texts
from .neo4j_client import create_chunk_node, run_cypher
from .config import CHUNK_SIZE, CHUNK_OVERLAP
import numpy as np

def ingest_text(text: str, source: str = 'notes', chunk_size: int = None, overlap: int = None) -> int:
    chunk_size = chunk_size or CHUNK_SIZE
    overlap = overlap or CHUNK_OVERLAP
    chunks = chunk_text(text, chunk_size, overlap)
    if not chunks:
        return 0
    embeddings = embed_texts(chunks)
    for ch, emb in zip(chunks, embeddings):
        create_chunk_node(ch, emb, source=source)
    # create naive similarity edges (pairwise for small graphs)
    _create_similarity_edges()
    return len(chunks)

def ingest_pdf_bytes(b: bytes, source: str = 'pdf', chunk_size: int = None, overlap: int = None) -> int:
    txt = extract_text_from_pdf_bytes(b)
    txt = clean_text(txt)
    return ingest_text(txt, source=source, chunk_size=chunk_size, overlap=overlap)

def _create_similarity_edges(threshold: float = 0.75):
    # naive O(N^2) pairing for small datasets: create SIMILAR_TO relationships
    rows = run_cypher('MATCH (c:Chunk) RETURN c.id AS id, c.embedding AS emb')
    items = []
    for r in rows:
        emb = r.get('emb') or []
        items.append((r['id'], np.array(emb, dtype=float)))
    for i in range(len(items)):
        id_i, vi = items[i]
        for j in range(i+1, len(items)):
            id_j, vj = items[j]
            denom = (np.linalg.norm(vi)*np.linalg.norm(vj))
            sim = float(np.dot(vi, vj)/denom) if denom!=0 else 0.0
            if sim >= threshold:
                run_cypher('MATCH (a:Chunk {id:$a}), (b:Chunk {id:$b}) MERGE (a)-[r:SIMILAR_TO]->(b) SET r.score=$score', {'a': id_i, 'b': id_j, 'score': float(sim)})
