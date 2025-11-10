"""
Top-level service that orchestrates RAG + real-time + LLM hybrid reasoning.
This is the unified interface used by the Streamlit frontend.
"""

from chains.hybrid_chain import hybrid_response
from utils.response_modes import format_response
from utils.logger import get_logger

logger = get_logger("genai_service")


def answer_query(user_query: str, lat: float, lon: float, mode: str = "concise"):
    """
    Handles the entire reasoning pipeline:
    - Uses RAG (vectorstore knowledge)
    - Integrates live weather data when relevant
    - Generates an LLM-based contextual response
    """

    try:
        # ✅ Step 1 — Get hybrid reasoning output (internally merges RAG + Weather)
        raw_answer = hybrid_response(user_query, mode=mode)

        # ✅ Step 2 — Format the response for display (concise or detailed)
        formatted_answer = format_response(raw_answer, mode=mode)

        # ✅ Step 3 — Add metadata (for Streamlit dashboard insights)
        meta = {
            "source": "Hybrid (RAG + Real-time Weather)",
            "query_mode": mode,
            "includes_weather": any(
                k in user_query.lower()
                for k in ["weather", "rain", "temperature", "climate", "forecast"]
            ),
        }

        return formatted_answer, meta

    except Exception as e:
        logger.error("❌ Hybrid chain failed: %s", e)
        error_msg = "⚠️ Sorry — an internal error occurred while generating your answer."
        return error_msg, {"error": str(e), "status": "failed"}