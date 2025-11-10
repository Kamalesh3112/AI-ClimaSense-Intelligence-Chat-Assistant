# services/llm_client.py
from langchain_openai import ChatOpenAI
from config.config import OPENAI_API_KEY, OPENAI_API_BASE, OPENAI_API_MODEL

def get_llm(temperature: float = 0.3):
    """
    Returns a ChatOpenAI-compatible client configured for Grok/xAI (GPT-OSS-20B).
    """
    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_API_BASE,      # important for xAI API
        model=OPENAI_API_MODEL,
        temperature=temperature,
        max_tokens=512
    )
    return llm