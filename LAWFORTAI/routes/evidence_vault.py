from fastapi import APIRouter, UploadFile, File, HTTPException
from datetime import datetime
from DataBase.mongo_models import db
import hashlib
from bson import ObjectId

router = APIRouter(prefix="/api/lawyer/evidence", tags=["Evidence Vault"])

@router.post("/upload")
async def upload_evidence(file: UploadFile = File(...)):
    content = await file.read()
    file_hash = hashlib.sha256(content).hexdigest()

    evidence = {
        "filename": file.filename,
        "hash": file_hash,
        "uploaded_at": datetime.utcnow()
    }

    result = await db.evidence_vault.insert_one(evidence)

    return {
        "id": str(result.inserted_id),
        "filename": file.filename,
        "hash": file_hash,
        "status": "uploaded"
    }

@router.get("/all")
async def get_all_evidence():
    evidence_list = await db.evidence_vault.find().to_list(100)
    for e in evidence_list:
        e["_id"] = str(e["_id"])
    return evidence_list

@router.delete("/{evidence_id}")
async def delete_evidence(evidence_id: str):
    await db.evidence_vault.delete_one({"_id": ObjectId(evidence_id)})
    return {"status": "deleted"}
