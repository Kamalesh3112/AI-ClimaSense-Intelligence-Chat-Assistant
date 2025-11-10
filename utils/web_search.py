import requests
import os

def perform_web_search(query):
    """
    Perform a live web search using Serper.dev or DuckDuckGo API.
    """
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        return "⚠️ Web search API key missing. Please add SERPER_API_KEY to .env"

    headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
    payload = {"q": query, "num": 5}
    response = requests.post("https://google.serper.dev/search", headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        results = [f"🔹 **{i['title']}**: {i['link']}" for i in data.get("organic", [])[:5]]
        return "\n\n".join(results)
    else:
        return f"❌ Web search failed ({response.status_code}): {response.text}"