from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

from ai.gemini import gemini_chat
from nlp.engine import process_query
from DataBase.mongo_models import save_query, save_chat_history, get_chat_history
from routes.fir_router import router as fir_router
from routes.universal_actions import router as universal_router
from nlp.chat_intelligence import get_session, handle_followup

# 🔥 Routers
from routes.lawyer_router import router as lawyer_router
from auth.routes import router as auth_router

# -------------------- APP INIT --------------------
app = FastAPI(title="LawFort AI Backend")

# -------------------- ROUTERS --------------------
app.include_router(auth_router, prefix="/api/auth")
app.include_router(universal_router, prefix="/api")
app.include_router(fir_router, prefix="/api")
app.include_router(lawyer_router, prefix="/api")

# -------------------- CORS --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- LOGGING --------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("LawFortAI")

# -------------------- ROUTERS --------------------
app.include_router(auth_router, prefix="/api/auth")   # 🔥 FIX
app.include_router(universal_router, prefix="/api")
app.include_router(fir_router, prefix="/api")

# -------------------- MODELS --------------------
class Query(BaseModel):
    query: str

# -------------------- ROOT --------------------
@app.get("/")
def root():
    return {"status": "LawFort AI running"}

# -------------------- TEXT QUERY --------------------
@app.post("/text-query")
def text_query(data: Query, request: Request):
    user_text = data.query.strip()
    user_id = request.client.host
    session = get_session(user_id)

    logger.info(f"Text query: {user_text} from {user_id}")

    # ---------- GREETINGS ----------
    if user_text.lower() in ["hi", "hello", "hey", "good morning", "good evening"]:
        try:
            greet = gemini_chat("Greet the user warmly like a friendly cyber law assistant.")
            if greet:
                session["last_answer"] = greet
                save_chat_history("guest", "user", user_text)
                save_chat_history("guest", "assistant", greet)
                return {"answer": greet, "source": "greeting"}
        except:
            pass

    # ---------- FOLLOW-UP HANDLING ----------
    followup = handle_followup(user_text, session)
    if followup:
        session["last_answer"] = followup
        save_chat_history("guest", "user", user_text)
        save_chat_history("guest", "assistant", followup)
        return {"answer": followup, "source": "follow-up"}

    # ---------- GEMINI (PRIMARY) ----------
    try:
        gemini_reply = gemini_chat(user_text)
        if gemini_reply:
            session["last_answer"] = gemini_reply
            session["last_topic"] = "conversation"

            save_chat_history("guest", "user", user_text)
            save_chat_history("guest", "assistant", gemini_reply)

            return {"answer": gemini_reply, "source": "gemini"}
    except Exception as e:
        logger.error(f"Gemini error: {e}")

    # ---------- LEGAL ENGINE (BACKUP) ----------
    try:
        law, confidence, method = process_query(user_text)
        if law:
            answer = law["summary"]
            session["last_answer"] = answer
            session["last_topic"] = "law"

            save_chat_history("guest", "user", user_text)
            save_chat_history("guest", "assistant", answer)

            save_query(
                user_text,
                answer,
                law.get("act"),
                law.get("section")
            )

            return {
                "answer": answer,
                "confidence": round(confidence, 2),
                "method": method,
                "source": "legal-engine",
                "follow_up": "You can ask for steps, helpline, or FIR."
            }
    except Exception as e:
        logger.error(f"Legal engine error: {e}")

    # ---------- FINAL FALLBACK (GEMINI POWERED) ----------
    try:
        fallback_prompt = f"""
User said: "{user_text}"

Respond like a friendly cyber law assistant.
Be empathetic, interactive, and natural.
Do NOT repeat generic lines.
Ask a helpful question.
"""
        fallback_reply = gemini_chat(fallback_prompt)
        if fallback_reply:
            session["last_answer"] = fallback_reply
            save_chat_history("guest", "user", user_text)
            save_chat_history("guest", "assistant", fallback_reply)
            return {"answer": fallback_reply, "source": "fallback-gemini"}
    except:
        pass

    # ---------- HARD FALLBACK ----------
    hard_fallback = "I’m here to help. Can you explain what happened?"
    session["last_answer"] = hard_fallback
    save_chat_history("guest", "user", user_text)
    save_chat_history("guest", "assistant", hard_fallback)

    return {"answer": hard_fallback, "source": "hard-fallback"}

# -------------------- CHAT HISTORY API --------------------
@app.get("/chat/history/{user_id}")
def chat_history(user_id: str):
    return {"history": get_chat_history(user_id)}
