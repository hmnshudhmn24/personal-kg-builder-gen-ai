# src/neo4j_client.py
from neo4j import GraphDatabase, basic_auth
import json, hashlib, os
import numpy as np
from .config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

_driver = None

def get_driver():
    global _driver
    if _driver is None:
        _driver = GraphDatabase.driver(NEO4J_URI, auth=basic_auth(NEO4J_USER, NEO4J_PASSWORD))
    return _driver

def _node_id_from(text: str, source: str):
    h = hashlib.sha1(f"{source}:{text[:200]}".encode('utf-8')).hexdigest()
    return h

def create_chunk_node(text: str, embedding: list, source: str = 'notes', metadata: dict = None):
    driver = get_driver()
    node_id = _node_id_from(text, source)
    meta = metadata or {}
    with driver.session() as session:
        session.run(
            """
            MERGE (c:Chunk {id:$id})
            SET c.text = $text, c.source = $source, c.metadata = $meta, c.embedding = $embedding
            """,
            id=node_id, text=text, source=source, meta=json.dumps(meta), embedding=embedding
        )
    return node_id

def run_cypher(query: str, params: dict = None):
    driver = get_driver()
    with driver.session() as session:
        rows = session.run(query, params or {}).data()
    return rows

def get_stats():
    driver = get_driver()
    with driver.session() as session:
        nodes = session.run("MATCH (c:Chunk) RETURN count(c) AS c").single().get('c')
        edges = session.run("MATCH ()-[r:SIMILAR_TO]->() RETURN count(r) AS r").single().get('r')
    return {'nodes': int(nodes or 0), 'similar_edges': int(edges or 0)}

def export_recent_subgraph_image(limit: int = 50, out_path: str = '/tmp/pg_subgraph.png') -> str:
    try:
        import networkx as nx
        import matplotlib.pyplot as plt
    except Exception:
        return ''
    driver = get_driver()
    with driver.session() as session:
        rows = session.run('MATCH (c:Chunk) RETURN c.id AS id, c.text AS text LIMIT $limit', {'limit': limit}).data()
        ids = [r['id'] for r in rows]
        if not ids:
            return ''
        rels = session.run('MATCH (a:Chunk)-[r:SIMILAR_TO]->(b:Chunk) WHERE a.id IN $ids AND b.id IN $ids RETURN a.id AS a, b.id AS b, r.score AS score', {'ids': ids}).data()
    G = nx.DiGraph()
    for r in rows:
        label = (r['text'][:60] + '...') if r.get('text') else r['id']
        G.add_node(r['id'], label=label)
    for rel in rels:
        G.add_edge(rel['a'], rel['b'], weight=rel.get('score', 0.0))
    plt.figure(figsize=(10,8))
    pos = nx.spring_layout(G, k=0.5, seed=42)
    labels = {n: G.nodes[n]['label'] for n in G.nodes()}
    nx.draw(G, pos, with_labels=False, node_size=300, arrows=True)
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    return out_path
