from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from strategy import hash_password, verify_password, create_access_token
from jose import JWTError, jwt
from config import settings
from pymongo import MongoClient
from pydantic import BaseModel, Field


import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

router = APIRouter()

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB]
users_collection = db["users"]

class User(BaseModel):
    username: str = Field(default=None)
    password: str = Field(default=None)

@router.post("/register", tags=["auth"], description="Register a new user", summary="Register a new user")
async def register(user: User):
    hashed_password = hash_password(user.password)
    user_db = users_collection.find_one({"username": user.username})
    if user_db:
        raise HTTPException(status_code=400, detail="User already exists")
    result = users_collection.insert_one({"username": user.username, "hashed_password": hashed_password})

    return {"message": "User registered successfully"}

@router.post("/token", tags=["auth"], description="Login a user", summary="Login a user")
async def login(form_data: User = Depends()):
    user = users_collection.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user["username"], "id": str(user["_id"])})
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: str = payload.get("id")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    return {"username": username, "id": user_id}