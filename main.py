from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

from auth.routes import router as auth_router
from nlp.engine import process_query
from voice.stt import voice_file_to_text, live_voice_to_text
from voice.tts import speak_text
from DataBase.mongo_models import save_query, save_chat_history, get_chat_history

# -------------------- LOGGING --------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("LawFortAI")

# -------------------- APP INIT --------------------
app = FastAPI(title="LawFort AI Backend")

# -------------------- CORS --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev mode
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- ROUTERS --------------------
app.include_router(auth_router, prefix="/api/auth")

# -------------------- MODELS --------------------
class Query(BaseModel):
    query: str

# -------------------- SMALL TALK --------------------
GREETINGS = {
    "hi", "hello", "hey", "hii", "hai",
    "good morning", "good afternoon", "good evening"
}

def is_greeting(text: str) -> bool:
    return text.lower().strip() in GREETINGS

# -------------------- ROOT --------------------
@app.get("/")
def root():
    return {"status": "LawFort AI running"}

# -------------------- TEXT QUERY --------------------
@app.post("/text-query")
def text_query(data: Query, request: Request):
    user_text = data.query.strip()
    logger.info(f"Text query: {user_text} from {request.client.host}")

    # 🥇 Layer 1 — Greeting
    if is_greeting(user_text):
        reply = "Hi 👋 I’m your Cyber & Legal Assistant. How can I help you today?"

        save_chat_history("guest", "user", user_text)
        save_chat_history("guest", "assistant", reply)

        return {"answer": reply}

    try:
        # 🥈 Layer 2 — Legal AI
        law, confidence, method = process_query(user_text)

        if law:
            answer = law["summary"]

            save_chat_history("guest", "user", user_text)
            save_chat_history("guest", "assistant", answer)

            save_query(user_text, answer, law["act"], law["section"])

            return {
                "answer": answer,
                "act": law["act"],
                "section": law["section"],
                "confidence": round(confidence, 2),
                "method": method
            }

        # 🥉 Layer 3 — Smart fallback
        fallback = (
            "I couldn’t find an exact legal section for that.\n"
            "Try asking about cybercrime, data breach, IT Act, or online fraud."
        )

        save_chat_history("guest", "user", user_text)
        save_chat_history("guest", "assistant", fallback)

        return {"answer": fallback}

    except Exception as e:
        logger.error(f"Text query error: {e}")

        safe_reply = (
            "Something went wrong internally. "
            "Please try again or ask a different legal question."
        )

        save_chat_history("guest", "assistant", safe_reply)
        return {"answer": safe_reply}

# -------------------- CHAT HISTORY --------------------
@app.get("/chat/history/{user_id}")
def chat_history(user_id: str):
    return {"history": get_chat_history(user_id)}
