from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from utils.role_guard import lawyer_only
from DataBase.mongo_models import db
from datetime import datetime
import hashlib

router = APIRouter(prefix="/api/lawyer", tags=["Lawyer Tools"])

# =========================
# CASE NOTEBOOK (CRUD)
# =========================

@router.post("/cases")
async def create_case(data: dict, user=Depends(lawyer_only)):
    data["lawyer_id"] = user["sub"]
    data["created_at"] = datetime.utcnow()
    result = await db.case_notebooks.insert_one(data)
    return {"id": str(result.inserted_id)}

@router.get("/cases")
async def get_cases(user=Depends(lawyer_only)):
    cases = await db.case_notebooks.find({"lawyer_id": user["sub"]}).to_list(100)
    return cases

@router.get("/cases/{case_id}")
async def get_case(case_id: str, user=Depends(lawyer_only)):
    case = await db.case_notebooks.find_one({"_id": case_id, "lawyer_id": user["sub"]})
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case

@router.put("/cases/{case_id}")
async def update_case(case_id: str, data: dict, user=Depends(lawyer_only)):
    await db.case_notebooks.update_one(
        {"_id": case_id, "lawyer_id": user["sub"]},
        {"$set": data}
    )
    return {"status": "updated"}

@router.delete("/cases/{case_id}")
async def delete_case(case_id: str, user=Depends(lawyer_only)):
    await db.case_notebooks.delete_one({"_id": case_id, "lawyer_id": user["sub"]})
    return {"status": "deleted"}

# =========================
# DIGITAL EVIDENCE VAULT
# =========================

@router.post("/evidence/upload")
async def upload_evidence(file: UploadFile = File(...), user=Depends(lawyer_only)):
    content = await file.read()
    file_hash = hashlib.sha256(content).hexdigest()

    evidence = {
        "filename": file.filename,
        "hash": file_hash,
        "uploaded_at": datetime.utcnow(),
        "lawyer_id": user["sub"]
    }

    await db.evidence.insert_one(evidence)
    return {"status": "uploaded", "hash": file_hash}

@router.get("/evidence")
async def get_all_evidence(user=Depends(lawyer_only)):
    items = await db.evidence.find({"lawyer_id": user["sub"]}).to_list(100)
    return items

# =========================
# CASE ROADMAP
# =========================

@router.post("/roadmap")
async def create_roadmap(data: dict, user=Depends(lawyer_only)):
    data["lawyer_id"] = user["sub"]
    data["created_at"] = datetime.utcnow()
    await db.roadmaps.insert_one(data)
    return {"status": "created"}

@router.get("/roadmap/{case_id}")
async def get_roadmap(case_id: str, user=Depends(lawyer_only)):
    roadmap = await db.roadmaps.find({
        "case_id": case_id,
        "lawyer_id": user["sub"]
    }).to_list(100)
    return roadmap

# =========================
# LEGAL PREP TOOLS
# =========================

@router.post("/summary")
async def generate_summary(data: dict, user=Depends(lawyer_only)):
    return {"summary": "AI summary will be generated here"}

@router.post("/draft")
async def generate_draft(data: dict, user=Depends(lawyer_only)):
    return {"draft": "Legal draft will be generated here"}

# =========================
# CLIENT MANAGER
# =========================

@router.post("/clients")
async def create_client(data: dict, user=Depends(lawyer_only)):
    data["lawyer_id"] = user["sub"]
    data["created_at"] = datetime.utcnow()
    result = await db.clients.insert_one(data)
    return {"id": str(result.inserted_id)}

@router.get("/clients")
async def get_clients(user=Depends(lawyer_only)):
    clients = await db.clients.find({"lawyer_id": user["sub"]}).to_list(100)
    return clients

# =========================
# INVESTIGATION TIMELINE
# =========================

@router.post("/timeline")
async def create_timeline_event(data: dict, user=Depends(lawyer_only)):
    data["lawyer_id"] = user["sub"]
    data["created_at"] = datetime.utcnow()
    await db.timelines.insert_one(data)
    return {"status": "created"}

@router.get("/timeline/{case_id}")
async def get_timeline(case_id: str, user=Depends(lawyer_only)):
    timeline = await db.timelines.find({
        "case_id": case_id,
        "lawyer_id": user["sub"]
    }).to_list(100)
    return timeline
