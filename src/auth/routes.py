from fastapi import APIRouter,Depends,HTTPException,status
from .schemas import create_user_schema,login_user_schema,update_user_schema,user_response_model
from src.db.main import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from .services import user_services
from .models import user_model
from .utils import verify_pass,encode_token,decode_token
from fastapi.responses import JSONResponse,Response
from datetime import timedelta
from .dependencies import RefreshTokenBearer,AccessTokenBearer
from src.db.redis import add_to_redis

REFRESH_TOKEN_EXPIRY = 86400

auth_router = APIRouter()
user_services = user_services()

@auth_router.post("/signup",response_model=user_response_model,status_code=status.HTTP_201_CREATED)
async def create_user_account(user:create_user_schema,session:AsyncSession = Depends(get_session)):
    new_user = await user_services.get_user_by_email(user.email,session)
    if new_user is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user already exists")
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
    await add_to_redis(jti=token_details['jti'])
    return "Succesfully logged out"


@auth_router.patch("/update",response_model=user_response_model,status_code=status.HTTP_200_OK)
async def update_user(id:str,user:update_user_schema,session:AsyncSession = Depends(get_session)):
    updated_user = await user_services.update_user(id,user,session)
    if updated_user is not None:
        return updated_user
    raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED)


@auth_router.delete("/delete",response_model=str,status_code=status.HTTP_200_OK)
async def delete_user(id:str,session:AsyncSession = Depends(get_session)):
    message = await user_services.delete_user(id,session)
    if message is not None:
        return message
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not exists")
    
    
    