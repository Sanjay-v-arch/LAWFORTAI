# backend/DataBase/mongo_models.py

from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

# Mongo URI (move to .env later if you want)
MONGO_URI = "mongodb+srv://sanjayofficial1302_db_user:y9WHTmkKdRkNytyk@lawfortai.jw3jj5k.mongodb.net/?appName=LAWFORTAI"

client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsAllowInvalidCertificates=True
)

db = client["LawFortAI"]

# Collections
query_collection = db["queries"]
chat_collection = db["chat_history"]

# -------------------- SAVE QUERY --------------------
def save_query(user_query: str, answer: str, act: str = None, section: str = None):
    try:
        query_collection.insert_one({
            "query": user_query,
            "answer": answer,
            "act": act,
            "section": section,
            "created_at": datetime.utcnow()
        })
    except Exception as e:
        print(f"MongoDB save_query error: {e}")

# -------------------- SAVE CHAT --------------------
def save_chat_history(user_id: str, role: str, message: str):
    try:
        chat_collection.insert_one({
            "user_id": user_id,
            "role": role,   # "user" or "assistant"
            "message": message,
            "created_at": datetime.utcnow()
        })
    except Exception as e:
        print(f"MongoDB save_chat_history error: {e}")

# -------------------- GET CHAT --------------------
def get_chat_history(user_id: str, limit: int = 20):
    try:
        chats = chat_collection.find(
            {"user_id": user_id}
        ).sort("created_at", -1).limit(limit)

        return list(chats)[::-1]  # oldest → newest
    except Exception as e:
        print(f"MongoDB get_chat_history error: {e}")
        return []
