from fastapi import APIRouter, HTTPException, Depends
from config import settings
from pydantic import BaseModel, Field
from typing import Optional, Union
import httpx
from pymongo import MongoClient
from bson import ObjectId

from routers.auth import get_current_user

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB]
favorites_collection = db["favorites"]

router = APIRouter()

BASE_URL = settings.BASE_URL + "favorites"

def convert_objectid_to_str(doc):
    if doc is None:
        return None
    if isinstance(doc, dict):
        result = {}
        for key, value in doc.items():
            if isinstance(value, ObjectId):
                result[key] = str(value)
            elif isinstance(value, dict):
                result[key] = convert_objectid_to_str(value)
            elif isinstance(value, list):
                result[key] = [convert_objectid_to_str(item) if isinstance(item, (dict, ObjectId)) else item for item in value]
            else:
                result[key] = value
        return result
    return doc


@router.get("/favorites", tags=["favorites"], description="Get all favorites", summary="Get all favorites, to use this feature you need to be authenticated")
async def get_favorites(current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    favorites = favorites_collection.find({"user_id": user_id})
    return [convert_objectid_to_str(favorite) for favorite in favorites]

@router.get("/favorites/{type}", tags=["favorites"], description="Get a favorite", summary="Get a favorite, to use this feature you need to be authenticated")
async def get_favorite(type: str, current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    favorite = favorites_collection.find_one({"user_id": user_id, "type": type})
    return convert_objectid_to_str(favorite)

@router.post("/favorites/{type}", tags=["favorites"], description="Add a favorite", summary="Add a favorite")
async def add_favorite(item_id: str, type: str, current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    favorite = favorites_collection.find_one({"user_id": user_id, "type": type})
    if favorite:
        raise HTTPException(status_code=400, detail="Favorite already exists")
    favorites_collection.insert_one({"user_id": user_id, "type": type, "item_id": item_id})
    return {"message": "Favorite added successfully"}
