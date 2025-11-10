"""
Hybrid Chain — Merges RAG (static reports) with live weather data
to generate a unified AI-driven agricultural reasoning response.
"""

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from services.llm_client import get_llm
from chains.rag_chain import get_rag_response
from chains.weather_chain import get_weather_data


def build_hybrid_chain():
    """
    Build a unified hybrid chain that merges:
      - Static RAG knowledge
      - Live weather data context
      - User query + reasoning mode
    """
    llm = get_llm()

    # ✅ Use PromptTemplate (works well with Groq / OpenAI-compatible LLMs)
    prompt = PromptTemplate(
        input_variables=["rag_context", "weather_context", "user_query", "mode"],
        template=(
            "You are an agricultural and climate domain expert.\n\n"
            "STATIC KNOWLEDGE (from research reports, datasets, and studies):\n"
            "{rag_context}\n\n"
            "LIVE WEATHER DATA (real-time observations):\n"
            "{weather_context}\n\n"
            "MODE: {mode}\n\n"
            "USER QUESTION:\n{user_query}\n\n"
            "Generate a comprehensive, factual, and actionable response using both sources.\n"
            "Include practical insights relevant to Indian agro-climate conditions."
        ),
    )

    # ✅ Combine into a simple runnable LangChain chain
    chain = prompt | llm | StrOutputParser()
    return chain


def hybrid_response(user_query: str, mode: str = "detailed"):
    """
    Unified hybrid reasoning flow that combines:
      - Static RAG results (knowledge base)
      - Real-time weather insights (API-driven)
    """
    # Step 1 — Retrieve static knowledge context
    rag_output = get_rag_response(user_query) or "No relevant static data found."

    # Step 2 — Conditionally get live weather data if relevant
    weather_keywords = ["weather", "rain", "temperature", "humidity", "climate", "forecast"]
    if any(word in user_query.lower() for word in weather_keywords):
        weather_output = get_weather_data(user_query)
    else:
        weather_output = "Weather data not relevant for this query."

    # Step 3 — Build and run the hybrid chain
    chain = build_hybrid_chain()
    result = chain.invoke({
        "rag_context": rag_output,
        "weather_context": weather_output,
        "user_query": user_query,
        "mode": mode
    })

    return result