from redis.asyncio import Redis
from src.config import config

JTI_EXPIRY = 600

redis = Redis.from_url(config.REDIS_URL,decode_responses=True)

async def add_to_redis(jti:str):
    await redis.set(name=jti,value="revoked",ex=JTI_EXPIRY)

async def check_in_redis(jti:str)->bool:
    con = await redis.get(jti)
    return True if con else False