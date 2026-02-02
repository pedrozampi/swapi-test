from redis import asyncio as redis
from config import settings

redis_client = None

async def get_redis():
    global redis_client
    if redis_client is None:
        redis_url = settings.REDIS_URL
        redis_client = await redis.from_url(redis_url, decode_responses=True)
    return redis_client

async def get_cache(key: str):
    redis = await get_redis()
    return await redis.get(key)

async def set_cache(key: str, value: str, ex: int = 60):
    redis = await get_redis()
    return await redis.set(key, value, ex=ex)

async def delete_cache(key: str):
    redis = await get_redis()
    return await redis.delete(key)