from fastapi import APIRouter, HTTPException
from datetime import datetime
from DataBase.mongo_models import db
from bson import ObjectId

router = APIRouter(prefix="/api/lawyer/roadmap", tags=["Case Roadmap"])

@router.post("/create")
async def create_roadmap(data: dict):
    data["created_at"] = datetime.utcnow()
    result = await db.case_roadmaps.insert_one(data)
    return {"id": str(result.inserted_id), "status": "created"}

@router.get("/all")
async def get_all_roadmaps():
    roadmaps = await db.case_roadmaps.find().to_list(100)
    for r in roadmaps:
        r["_id"] = str(r["_id"])
    return roadmaps

@router.get("/{roadmap_id}")
async def get_roadmap(roadmap_id: str):
    roadmap = await db.case_roadmaps.find_one({"_id": ObjectId(roadmap_id)})
    if not roadmap:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    roadmap["_id"] = str(roadmap["_id"])
    return roadmap

@router.put("/{roadmap_id}")
async def update_roadmap(roadmap_id: str, data: dict):
    await db.case_roadmaps.update_one(
        {"_id": ObjectId(roadmap_id)},
        {"$set": data}
    )
    return {"status": "updated"}

@router.delete("/{roadmap_id}")
async def delete_roadmap(roadmap_id: str):
    await db.case_roadmaps.delete_one({"_id": ObjectId(roadmap_id)})
    return {"status": "deleted"}
