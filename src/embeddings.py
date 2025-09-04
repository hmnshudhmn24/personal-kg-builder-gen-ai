# src/embeddings.py
from typing import List
import os, logging
from .config import EMBEDDINGS_USE_OPENAI, OPENAI_API_KEY, OPENAI_EMBED_MODEL

logger = logging.getLogger(__name__)

if EMBEDDINGS_USE_OPENAI and OPENAI_API_KEY:
    import openai
    openai.api_key = OPENAI_API_KEY

def embed_texts(texts: List[str]) -> List[List[float]]:
    if EMBEDDINGS_USE_OPENAI and OPENAI_API_KEY:
        out = []
        for t in texts:
            try:
                resp = openai.Embeddings.create(model=OPENAI_EMBED_MODEL, input=t)
                vec = resp['data'][0]['embedding']
                out.append(vec)
            except Exception as e:
                logger.exception('OpenAI embedding failed, falling back: %s', e)
                out.append(_local_embed([t])[0])
        return out
    return _local_embed(texts)

def _local_embed(texts: List[str]):
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        arr = model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
        return arr.tolist()
    except Exception as e:
        logger.exception('Local embedding failed: %s', e)
        return [[0.0]*384 for _ in texts]
