# src/utils.py
import re
from typing import List
from pypdf import PdfReader

def clean_text(text: str) -> str:
    if not text:
        return ''
    t = text.replace('\r', ' ').replace('\t', ' ')
    t = re.sub(r'\s+', ' ', t)
    return t.strip()

def extract_text_from_pdf_bytes(b: bytes) -> str:
    try:
        reader = PdfReader(b)
        pages = [p.extract_text() or '' for p in reader.pages]
        return '\n\n'.join(pages)
    except Exception:
        try:
            return b.decode('utf-8', errors='ignore')
        except Exception:
            return ''

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    text = clean_text(text)
    if len(text) <= chunk_size:
        return [text]
    chunks = []
    start = 0
    L = len(text)
    while start < L:
        end = min(start + chunk_size, L)
        chunk = text[start:end]
        chunks.append(chunk.strip())
        start = end - overlap
        if start < 0:
            start = 0
    return [c for c in chunks if c]
