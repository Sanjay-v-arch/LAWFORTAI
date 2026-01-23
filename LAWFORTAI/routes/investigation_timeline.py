from fastapi import APIRouter, HTTPException
from datetime import datetime
from DataBase.mongo_models import db
from bson import ObjectId

router = APIRouter(prefix="/api/lawyer/timeline", tags=["Investigation Timeline"])

@router.post("/create")
async def create_event(data: dict):
    data["created_at"] = datetime.utcnow()
    result = await db.investigation_timelines.insert_one(data)
    return {"id": str(result.inserted_id), "status": "created"}

@router.get("/all")
async def get_all_events():
    events = await db.investigation_timelines.find().to_list(100)
    for e in events:
        e["_id"] = str(e["_id"])
    return events

@router.get("/{event_id}")
async def get_event(event_id: str):
    event = await db.investigation_timelines.find_one({"_id": ObjectId(event_id)})
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    event["_id"] = str(event["_id"])
    return event

@router.put("/{event_id}")
async def update_event(event_id: str, data: dict):
    await db.investigation_timelines.update_one(
        {"_id": ObjectId(event_id)},
        {"$set": data}
    )
    return {"status": "updated"}

@router.delete("/{event_id}")
async def delete_event(event_id: str):
    await db.investigation_timelines.delete_one({"_id": ObjectId(event_id)})
    return {"status": "deleted"}
