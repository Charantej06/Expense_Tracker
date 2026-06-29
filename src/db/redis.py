from redis.asyncio import Redis
from src.config import config

JTI_EXPIRY = 600
OTP_EXPIRY = 600

redis = Redis.from_url(config.REDIS_URL,decode_responses=True)

async def add_jti_to_redis(jti:str,email:str):
    await redis.set(name=f"jti:{email}",value="revoked",ex=JTI_EXPIRY)

async def check_jti_in_redis(jti:str,email:str)->bool:
    con = await redis.get(f"jti:{email}")
    return True if con is not None else False

#-------------------------------------------------------------------------------------------------

async def add_otp_to_redis(msg:str,email:str,otp:str):
    await redis.set(name=f'otp:{msg}:{email}',value=otp,ex=OTP_EXPIRY)

async def check_otp_in_redis(msg:str,email:str)->str:
    otp = await redis.get(f'otp:{msg}:{email}')
    return otp if otp is not None else None    

async def remove_otp_from_redis(msg:str,email:str):
    await redis.delete(f'otp:{msg}:{email}')

# -----------------------------------------------------------------------------------------------

async def add_userdata_to_redis(email:str,user_data:dict):
    await redis.set(name=f"new_user:{email}",value=user_data,ex=OTP_EXPIRY)

async def check_userdata_in_redis(email:str):
    user_data = await redis.get(f"new_user:{email}")
    return user_data if user_data is not None else None

async def remove_userdata_from_redis(email:str):
    await redis.delete(f"new_user:{email}")

# -----------------------------------------------------------------------------------------------