from fastapi import APIRouter, HTTPException
from datetime import datetime
from DataBase.mongo_models import db
from bson import ObjectId

router = APIRouter(prefix="/api/lawyer/clients", tags=["Client Manager"])

@router.post("/create")
async def create_client(data: dict):
    data["created_at"] = datetime.utcnow()
    result = await db.clients.insert_one(data)
    return {"id": str(result.inserted_id), "status": "created"}

@router.get("/all")
async def get_all_clients():
    clients = await db.clients.find().to_list(100)
    for c in clients:
        c["_id"] = str(c["_id"])
    return clients

@router.get("/{client_id}")
async def get_client(client_id: str):
    client = await db.clients.find_one({"_id": ObjectId(client_id)})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    client["_id"] = str(client["_id"])
    return client

@router.put("/{client_id}")
async def update_client(client_id: str, data: dict):
    await db.clients.update_one(
        {"_id": ObjectId(client_id)},
        {"$set": data}
    )
    return {"status": "updated"}

@router.delete("/{client_id}")
async def delete_client(client_id: str):
    await db.clients.delete_one({"_id": ObjectId(client_id)})
    return {"status": "deleted"}
