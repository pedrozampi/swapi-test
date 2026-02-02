from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    BASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    MONGO_URI: str
    MONGO_DB: str
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()