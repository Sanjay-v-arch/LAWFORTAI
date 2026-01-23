from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

# -------------------- APP INIT --------------------
app = FastAPI(title="LawFort AI Backend")

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

# -------------------- CORE LOGIC --------------------
from ai.gemini import gemini_chat
from nlp.engine import process_query
from nlp.chat_intelligence import get_session, handle_followup

# -------------------- DATABASE --------------------
from DataBase.mongo_models import (
    save_query,
    save_chat_history,
    get_chat_history,
)

# -------------------- AUTH & COMMON ROUTES --------------------
from auth.routes import router as auth_router
from routes.universal_actions import router as universal_router
from routes.fir_router import router as fir_router

# -------------------- LAWYER FEATURE ROUTES --------------------
from routes.lawyer_router import router as lawyer_router
from routes.case_notebook import router as case_notebook_router
from routes.evidence_vault import router as evidence_router
from routes.case_roadmap import router as roadmap_router
from routes.investigation_timeline import router as timeline_router
from routes.investigation_records import router as records_router
from routes.client_manager import router as client_router
from routes.cyber_law_intelligence import router as intelligence_router

# -------------------- REGISTER ROUTERS --------------------
app.include_router(auth_router, prefix="/api/auth")
app.include_router(universal_router, prefix="/api")
app.include_router(fir_router, prefix="/api")

# Lawyer-only APIs
app.include_router(lawyer_router)
app.include_router(case_notebook_router)
app.include_router(evidence_router)
app.include_router(roadmap_router)
app.include_router(timeline_router)
app.include_router(records_router)
app.include_router(client_router)
app.include_router(intelligence_router)

# -------------------- MODELS --------------------
class Query(BaseModel):
    query: str

# -------------------- ROOT --------------------
@app.get("/")
def root():
    return {"status": "LawFort AI running"}

# -------------------- CHATBOT --------------------
@app.post("/text-query")
def text_query(data: Query, request: Request):
    user_text = data.query.strip()
    user_id = request.client.host
    session = get_session(user_id)

    logger.info(f"Text query: {user_text} from {user_id}")

    # ---------- FOLLOW-UP ----------
    followup = handle_followup(user_text, session)
    if followup:
        session["last_answer"] = followup
        save_chat_history("guest", "user", user_text)
        save_chat_history("guest", "assistant", followup)
        return {"answer": followup, "source": "context"}

    # ---------- LEGAL ENGINE (FIRST) ----------
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
                law.get("section"),
            )

            return {
                "answer": answer,
                "confidence": round(confidence, 2),
                "method": method,
                "source": "legal-engine",
                "follow_up": "You can ask for recovery steps, helpline, or FIR.",
            }
    except Exception as e:
        logger.error(f"Legal engine error: {e}")

    # ---------- GEMINI (FALLBACK) ----------
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

    # ---------- FINAL FALLBACK ----------
    fallback = "I’m here to help. Tell me what happened."
    session["last_answer"] = fallback
    #save_chat_history("guest", "user", user_text)
    #save_chat_history("guest", "assistant", fallback)

    return {"answer": fallback, "source": "fallback"}

# -------------------- CHAT HISTORY --------------------
@app.get("/chat/history/{user_id}")
def chat_history(user_id: str):
    return {"history": get_chat_history(user_id)}
