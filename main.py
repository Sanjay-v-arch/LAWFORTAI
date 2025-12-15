from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from nlp.engine import process_query
from voice.stt import voice_file_to_text
from voice.tts import speak_text
from DataBase.mongo_models import save_query 

app = FastAPI(title="LawFort AI Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- TEXT QUERY --------------------
class Query(BaseModel):
    query: str

@app.get("/")
def root():
    return {"status": "LawFort AI running"}

@app.post("/text-query")
def text_query(data: Query):
    law, confidence, method = process_query(data.query)

    if not law:
        return {
            "answer": "Sorry, I couldn't find a relevant legal section.",
            "confidence": 0.0
        }

    return {
        "answer": law["summary"],
        "act": law["act"],
        "section": law["section"],
        "confidence": round(confidence, 2),
        "method": method
    }

# -------------------- VOICE QUERY --------------------
@app.post("/voice-query")
async def voice_query(file: UploadFile = File(...)):
    # Save uploaded audio
    file_location = f"voice/temp_audio.wav"
    with open(file_location, "wb") as f:
        f.write(await file.read())
    
    # Convert audio → text
    text_query = voice_file_to_text(file_location)

    # Process query through NLP engine
    law, confidence, method = process_query(text_query)

    if law:
        answer_text = law["summary"]
        act = law["act"]
        section = law["section"]
    else:
        answer_text = "Sorry, I couldn't find a relevant legal section."
        act = None
        section = None

    # Save conversation to MongoDB
    save_query(text_query, answer_text, act, section)

    # Convert text → speech
    audio_file = f"voice/response.wav"
    speak_text(answer_text, filename=audio_file)

    return {
        "heard": text_query,
        "answer": answer_text,
        "act": act,
        "section": section,
        "confidence": round(confidence, 2),
        "method": method,
        "audio_file": audio_file  # frontend can play this
    }

