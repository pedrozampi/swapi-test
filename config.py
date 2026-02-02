from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    BASE_URL: str = "https://swapi.dev/api/"
    SECRET_KEY: str = "sW4p1*"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    MONGO_URI: Optional[str] = None
    MONGO_DB: str = "starwars"
    MONGO_USERNAME: str = "admin"
    MONGO_PASSWORD: str = "admin123"
    MONGO_HOST: str = "localhost"
    MONGO_PORT: int = 27017
    REDIS_URL: str = "redis://localhost:6379"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()

# Construct MongoDB URI if not provided
if not settings.MONGO_URI:
    settings.MONGO_URI = f"mongodb://{settings.MONGO_USERNAME}:{settings.MONGO_PASSWORD}@{settings.MONGO_HOST}:{settings.MONGO_PORT}/{settings.MONGO_DB}?authSource=admin"