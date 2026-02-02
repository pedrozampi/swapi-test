from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from typing import Optional
from config import settings
from pymongo import MongoClient
from .auth import get_current_user
from datetime import datetime
from bson import ObjectId
router = APIRouter()

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB]
comments_collection = db["comments"]


class comment(BaseModel):
    content: str = Field(default=None)
    item_id: str = Field(default=None)
    item_type: str = Field(default=None)

class comment_update(BaseModel):
    content: Optional[str] = None

class comment_response(BaseModel):
    content: str
    created: str
    updated: Optional[str] = None
    user_id: str

class comments_response(BaseModel):
    comments: list[comment_response]
    total: int
    page: int
    limit: int

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

@router.post("/comments", tags=["comments"], description="Add a comment", summary="Add a comment")
async def add_comment(comment: comment, current_user: dict = Depends(get_current_user)):
    comments_collection.insert_one({**comment.model_dump(), "created": datetime.now().isoformat(), "updated": None, "user_id": ObjectId(current_user["id"])})
    return {"message": "Comment added successfully"}

@router.get("/comments", tags=["comments"], description="Get all comments", summary="Get all comments")
async def get_comments(item_id: str, item_type: str, page: int = 1, limit: int = 10, order_by: str = "created", order_direction: str = "asc") -> comments_response:
    comments = comments_collection.find({"item_id": item_id, "item_type": item_type}).skip((page - 1) * limit).limit(limit)
    if order_by:
        comments = sorted(comments, key=lambda x: getattr(x, order_by, ""), reverse=order_direction == "desc")
    return comments_response(comments=[convert_objectid_to_str(comment) for comment in comments], total=comments_collection.count_documents({"item_id": item_id, "item_type": item_type}), page=page, limit=limit)

@router.get("/comments/{comment_id}", tags=["comments"], description="Get a comment by ID", summary="Get a comment by ID")
async def get_comment(comment_id: str):
    comment_doc = comments_collection.find_one({"_id": ObjectId(comment_id)})
    if not comment_doc:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Comment not found")
    return convert_objectid_to_str(comment_doc)

@router.get("/comments/user/{user_id}", tags=["comments"], description="Get all comments by user ID", summary="Get all comments by user ID")
async def get_comments_by_user(user_id: str, page: int = 1, limit: int = 10, order_by: str = "created", order_direction: str = "asc") -> comments_response:
    comments = comments_collection.find({"user_id": ObjectId(user_id)}).skip((page - 1) * limit).limit(limit)
    if order_by:
        comments = sorted(comments, key=lambda x: getattr(x, order_by, ""), reverse=order_direction == "desc")
    return comments_response(comments=[convert_objectid_to_str(comment) for comment in comments], total=comments_collection.count_documents({"user_id": ObjectId(user_id)}), page=page, limit=limit)

@router.put("/comments/{comment_id}", tags=["comments"], description="Update a comment", summary="Update a comment")
async def update_comment(comment_id: str, comment: comment_update, current_user: dict = Depends(get_current_user)):
    result = comments_collection.update_one({"_id": ObjectId(comment_id), "user_id": ObjectId(current_user["id"])}, {"$set": {**comment.model_dump(), "updated": datetime.now().isoformat()}})
    if result.matched_count == 0:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Comment not found or you don't have permission to update it")
    return {"message": "Comment updated successfully"}

@router.delete("/comments/{comment_id}", tags=["comments"], description="Delete a comment", summary="Delete a comment")
async def delete_comment(comment_id: str, current_user: dict = Depends(get_current_user)):
    result = comments_collection.delete_one({"_id": ObjectId(comment_id), "user_id": ObjectId(current_user["id"])})
    if result.deleted_count == 0:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Comment not found or you don't have permission to delete it")
    return {"message": "Comment deleted successfully"}