"""
Simple web search utility using duckduckgo_search as fallback.
"""
from duckduckgo_search import ddg_answers, ddg
from typing import List
import requests
import os
from utils.logger import get_logger

logger = get_logger(__name__)
SERPER_KEY = os.getenv("SERPER_API_KEY")

def serper_search(q, max_results=5):
    if not SERPER_KEY:
        return None
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_KEY, "Content-Type": "application/json"}
    try:
        r = requests.post(url, headers=headers, json={"q": q, "num": max_results}, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logger.error("Serper search failed: %s", e)
        return None


def quick_search(query: str, max_results: int = 5) -> List[dict]:
    """
    Returns a list of search results with title and snippet.
    """
    try:
        results = ddg(query, max_results=max_results)
        out = []
        for r in results:
            out.append({"title": r.get("title"), "body": r.get("body"), "href": r.get("href")})
        return out
    except Exception:
        # fallback to ddg_answers
        try:
            ans = ddg_answers(query)
            return [{"title": query, "body": ans, "href": ""}]
        except Exception as e:
            return [{"title": "search_error", "body": str(e), "href": ""}]