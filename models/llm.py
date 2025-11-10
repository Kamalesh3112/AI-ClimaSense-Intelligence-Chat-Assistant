"""
LLM wrapper using LangChain ChatOpenAI (configured for GPT-OSS model).
If you want to use the openai library directly, you can adapt this file.
"""
import os
from langchain_openai import ChatOpenAI
from config.config import OPENAI_API_KEY, OPENAI_API_MODEL

def get_llm(temperature: float = 0.2, max_tokens: int = 1024):
    """
    Returns a LangChain ChatOpenAI instance configured for your model.
    """
    if not OPENAI_API_KEY:
        raise EnvironmentError("OPENAI_API_KEY not set in environment")
    # LangChain will pick up key from env var OPENAI_API_KEY by default.
    llm = ChatOpenAI(model=OPENAI_API_MODEL, temperature=temperature, max_tokens=max_tokens)
    return llm