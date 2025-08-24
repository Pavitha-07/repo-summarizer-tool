import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def call_ai(code: str, language: str) -> str:
    if not API_KEY:
        return "No API key found. Please set it in .env"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a code summarizer. Explain briefly what the given code does."},
            {"role": "user", "content": f"Language: {language}\n\nCode:\n{code}"}
        ]
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"API Error: {e}"

#Force utf-8 encoding & ignore invalid characters
LANGUAGE_HANDLERS = {
    ".py": lambda path, indent: f"{indent}{call_ai(open(path, encoding='utf-8', errors='ignore').read(), 'Python')}",
    ".js": lambda path, indent: f"{indent}{call_ai(open(path, encoding='utf-8', errors='ignore').read(), 'JavaScript')}",
    ".java": lambda path, indent: f"{indent}{call_ai(open(path, encoding='utf-8', errors='ignore').read(), 'Java')}",
}
