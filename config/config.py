"""
Configuration for API keys and settings.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# LLM (Groq / OpenAI-compatible)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.groq.com/openai/v1")
OPENAI_API_MODEL = os.getenv("OPENAI_API_MODEL", "llama-3.3-70b-versatile")

# Hugging Face (for diffusion)
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Vectorstore
VECTORSTORE_PATH = os.getenv("VECTORSTORE_PATH", "data/vectorstore/faiss_index")

# Weather
OPEN_METEO_BASE = "https://api.open-meteo.com/v1/forecast"

#Serper Google Search API Integration
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# App defaults
DEFAULT_LAT = float(os.getenv("DEFAULT_LAT", 13.0827))
DEFAULT_LON = float(os.getenv("DEFAULT_LON", 80.2707))