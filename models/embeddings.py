"""
Embeddings wrapper using HuggingFace / SentenceTransformers via LangChain.
"""
from langchain.embeddings import HuggingFaceEmbeddings
from config.constants import EMBEDDING_MODEL

def get_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)