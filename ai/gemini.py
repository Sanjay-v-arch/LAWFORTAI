import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# IMPORTANT: must be GOOGLE_API_KEY
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not found in environment")

genai.configure(api_key=API_KEY)

# Use a valid supported model
model = genai.GenerativeModel("models/gemini-1.5-flash")

SYSTEM_PROMPT = """
You are LawFort AI, a friendly cyber law assistant.
Be natural, empathetic, and helpful.
Do not repeat generic lines.
Guide users clearly.
"""

def gemini_chat(user_text: str) -> str | None:
    try:
        response = model.generate_content(
            f"{SYSTEM_PROMPT}\nUser: {user_text}\nAssistant:"
        )
        return response.text
    except Exception as e:
        print("Gemini error:", e)
        return None
