from fastapi import APIRouter, HTTPException
from datetime import datetime
from DataBase.mongo_models import db
from bson import ObjectId

router = APIRouter(prefix="/api/lawyer/records", tags=["Investigation Records"])

@router.post("/create")
async def create_record(data: dict):
    data["created_at"] = datetime.utcnow()
    result = await db.investigation_records.insert_one(data)
    return {"id": str(result.inserted_id), "status": "created"}

@router.get("/all")
async def get_all_records():
    records = await db.investigation_records.find().to_list(100)
    for r in records:
        r["_id"] = str(r["_id"])
    return records

@router.get("/{record_id}")
async def get_record(record_id: str):
    record = await db.investigation_records.find_one({"_id": ObjectId(record_id)})
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    record["_id"] = str(record["_id"])
    return record

@router.put("/{record_id}")
async def update_record(record_id: str, data: dict):
    await db.investigation_records.update_one(
        {"_id": ObjectId(record_id)},
        {"$set": data}
    )
    return {"status": "updated"}

@router.delete("/{record_id}")
async def delete_record(record_id: str):
    await db.investigation_records.delete_one({"_id": ObjectId(record_id)})
    return {"status": "deleted"}
