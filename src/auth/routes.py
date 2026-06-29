from fastapi import APIRouter,Depends,HTTPException,status
from .schemas import (create_user_schema,
                      login_user_schema,
                      update_user_schema,
                      user_response_model,
                      verify_new_user_schema,
                      reset_password_schema)
from src.db.main import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from .services import user_services
from .models import user_model
from .utils import verify_pass,encode_token,decode_token,hash_pass
from fastapi.responses import JSONResponse,Response
from datetime import timedelta
from .dependencies import RefreshTokenBearer,AccessTokenBearer
from src.db.redis import (add_jti_to_redis,
                          add_otp_to_redis,
                          check_otp_in_redis,
                          add_userdata_to_redis,
                          check_userdata_in_redis)
from src.emails.send_mails import send_verificatin_mail

REFRESH_TOKEN_EXPIRY = 86400

auth_router = APIRouter()
user_services = user_services()


@auth_router.post("/signup",status_code=status.HTTP_200_OK)
async def create_user_account(user:create_user_schema,session:AsyncSession = Depends(get_session)):
    new_user = await user_services.get_user_by_email(user.email,session)
    if new_user is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user already exists")
    await add_userdata_to_redis(
        email=user.email,
        user_data=user.model_dump_json()
    )
    otp = send_verificatin_mail(user.email)
    await add_otp_to_redis(msg="verify",email=user.email,otp=otp)



@auth_router.post("/verify_new_user_email",response_model=user_response_model,status_code=status.HTTP_201_CREATED)
async def verify_new_user_email(data:verify_new_user_schema,session:AsyncSession = Depends(get_session)):
    new_user = await user_services.get_user_by_email(data.email,session)
    if new_user is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user already exists")
    redis_otp = await check_otp_in_redis(msg="verify",email=data.email)
    if redis_otp is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="OTP Expired")
    if redis_otp != data.otp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid OTP")
    user_data = await check_userdata_in_redis(email=data.email)
    if user_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User data Expired")
    user = create_user_schema.model_validate_json(user_data)
    new_user = await user_services.create_user(user,session)
    return new_user



@auth_router.post("/login",status_code=status.HTTP_200_OK)
async def user_login(user:login_user_schema,session:AsyncSession = Depends(get_session)):
    user_data = await user_services.get_user_by_email(user.email,session)
    if user_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found")
    is_legit = verify_pass(user.password_hash,user_data.password_hash)
    if not is_legit:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Password")
    access_token = encode_token(
        user_data={
            "user_id":str(user_data.uid),
            "username":user_data.username,
            "email" : user_data.email
        }
    )
    refresh_token = encode_token(
        user_data={
            "user_id":str(user_data.uid),
            "username":user_data.username,
            "email" : user_data.email
        },
        expiry = timedelta(seconds=REFRESH_TOKEN_EXPIRY),
        refresh = True
    )
    return JSONResponse(
        content={
            "message":"Login successful",
            "access token":access_token,
            "refresh token":refresh_token,
            "user": {"email": user.email, "uid": str(user_data.uid)}
        }
    )



@auth_router.get("/refreshtoken")
async def Refresh_token(session:AsyncSession = Depends(get_session),token_details:dict = Depends(RefreshTokenBearer())):
    access_token = encode_token(
        user_data={
            "user_id":token_details['user']['user_id'],
            "username":token_details['user']['username'],
            "email" : token_details["user"]['email']
        }
    )
    return JSONResponse(
        content={
            "access token":access_token
        }
    )
    

@auth_router.get("/logout")
async def user_logout(session:AsyncSession = Depends(get_session),token_details:dict = Depends(AccessTokenBearer())):
    await add_jti_to_redis(jti=token_details['jti'],email=token_details['user']['email'])
    return "Succesfully logged out"


@auth_router.post("/resetpassword")
async def reset_password(data:reset_password_schema,session:AsyncSession = Depends(get_session),token_details:dict = Depends(AccessTokenBearer())):
    user = await user_services.get_user_by_email(token_details['user']['email'],session)
    if verify_pass(data.old_password,user.password_hash):
        if data.new_password != data.confirm_password:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="mismatch of new nad confirm password")
        user.password_hash = hash_pass(data.new_password)
        await session.commit()
        return "Successfully reseted password"
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Old Password")



@auth_router.patch("/update",response_model=user_response_model,status_code=status.HTTP_200_OK)
async def update_user(id:str,user:update_user_schema,session:AsyncSession = Depends(get_session),token_details:dict = Depends(AccessTokenBearer())):
    updated_user = await user_services.update_user(id,user,session)
    if updated_user is not None:
        return updated_user
    raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED)


@auth_router.delete("/delete",response_model=str,status_code=status.HTTP_200_OK)
async def delete_user(session:AsyncSession = Depends(get_session),token_details:dict = Depends(AccessTokenBearer())):
    message = await user_services.delete_user(token_details["user"]["user_id"],session)
    if message is not None:
        await add_jti_to_redis(jti=token_details['jti'],email=token_details['user']['email'])
        return message
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not exists")
    
    
    