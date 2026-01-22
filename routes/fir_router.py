from fastapi import APIRouter, Request
from datetime import datetime
from DataBase.mongo_models import db

router = APIRouter()

fir_logs = db["fir_action_logs"]

@router.post("/file-complaint")
async def file_complaint(data: dict, request: Request):
    fir_logs.insert_one({
        "contact": data.get("contact", "guest"),
        "role": data.get("role", "citizen"),
        "action": "FIR Complaint Redirect",
        "ip": request.client.host,
        "timestamp": datetime.utcnow()
    })

    return {
        "status": "ok",
        "message": "FIR redirect logged"
    }
