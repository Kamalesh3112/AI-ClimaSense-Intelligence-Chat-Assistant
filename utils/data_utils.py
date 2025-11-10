"""
Data utilities: chunking, embedding ingestion helper, simple realtime API fetchers.
"""
import os
import math
import json
import requests
from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from config.constants import CHUNK_SIZE, FAISS_INDEX_DIR, KNOWLEDGE_DIR, EMBEDDING_MODEL

def chunk_text(text: str, size: int = CHUNK_SIZE) -> List[str]:
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start = end
    return chunks

def build_vectorstore_from_local_docs():
    import os
    from langchain_community.vectorstores import FAISS
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    kb_path = "data/knowledge_base"
    vs_path = "data/vectorstore"

    os.makedirs(vs_path, exist_ok=True)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    docs = []
    for filename in os.listdir(kb_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(kb_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
                docs.append(text)

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.create_documents(docs)

    # Build FAISS index
    print("🔍 Generating embeddings and creating FAISS index...")
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(vs_path)

    print("✅ Vectorstore successfully built and saved in:", vs_path)

def get_realtime_weather(lat: float, lon: float):
    """
    Simple wrapper to fetch basic weather forecast from Open-Meteo API.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,precipitation",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto"
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()

def get_realtime_weather_summary(lat: float, lon: float) -> str:
    """
    Produce a human-readable summary for quick context insertion into LLM prompt.
    """
    data = get_realtime_weather(lat, lon)
    daily = data.get("daily", {})
    temps_max = daily.get("temperature_2m_max", [])
    temps_min = daily.get("temperature_2m_min", [])
    precip = daily.get("precipitation_sum", [])
    summary_lines = []
    if temps_max:
        summary_lines.append(f"Daily max temps next days: {temps_max[:5]}")
    if temps_min:
        summary_lines.append(f"Daily min temps next days: {temps_min[:5]}")
    if precip:
        summary_lines.append(f"Daily precipitation sum next days: {precip[:5]}")
    return "\n".join(summary_lines) if summary_lines else "No weather summary available."