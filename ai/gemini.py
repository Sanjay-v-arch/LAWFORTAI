import os
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

SYSTEM_PROMPT = """
You are LawFort AI, a friendly cyber law assistant.
Talk naturally, be interactive, empathetic, and helpful.
Do not repeat generic lines.
Ask relevant questions.
"""

def gemini_chat(user_text: str) -> str | None:
    if not GEMINI_API_KEY:
        print("❌ Gemini API key missing")
        return None

    # ✅ Correct & supported endpoint
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "contents": [
            {
                "parts": [{"text": f"{SYSTEM_PROMPT}\n\nUser: {user_text}\nAssistant:"}]
            }
        ]
    }

    try:
        response = requests.post(url, json=payload, timeout=20)
        print("Gemini status:", response.status_code)
        print("Gemini raw:", response.text)

        response.raise_for_status()
        data = response.json()

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        print("❌ Gemini error:", e)
        return None
