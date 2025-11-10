# test_groq_api.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

r = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json",
    },
    json={
        "model": os.getenv("OPENAI_API_MODEL"),
        "messages": [{"role": "user", "content": "Say hello from Llama 3.3 70B on Groq"}],
    },
)

print("Status:", r.status_code)
print("Response:", r.text[:400])