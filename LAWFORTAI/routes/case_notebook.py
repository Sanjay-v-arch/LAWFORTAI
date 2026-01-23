from fastapi import APIRouter, HTTPException
from datetime import datetime
from DataBase.mongo_models import db
from bson import ObjectId

router = APIRouter(prefix="/api/lawyer/notebook", tags=["Case Notebook"])

# Create new case note
@router.post("/create")
async def create_note(data: dict):
    data["created_at"] = datetime.utcnow()
    result = await db.case_notebooks.insert_one(data)
    return {"id": str(result.inserted_id), "status": "created"}

# Get all notes
@router.get("/all")
async def get_all_notes():
    notes = await db.case_notebooks.find().to_list(100)
    for n in notes:
        n["_id"] = str(n["_id"])
    return notes

# Get single note
@router.get("/{note_id}")
async def get_note(note_id: str):
    note = await db.case_notebooks.find_one({"_id": ObjectId(note_id)})
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note["_id"] = str(note["_id"])
    return note

# Update note
@router.put("/{note_id}")
async def update_note(note_id: str, data: dict):
    await db.case_notebooks.update_one(
        {"_id": ObjectId(note_id)},
        {"$set": data}
    )
    return {"status": "updated"}

# Delete note
@router.delete("/{note_id}")
async def delete_note(note_id: str):
    await db.case_notebooks.delete_one({"_id": ObjectId(note_id)})
    return {"status": "deleted"}
