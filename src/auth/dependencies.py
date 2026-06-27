from fastapi.security import HTTPBearer
from .utils import decode_token
from fastapi import HTTPException,status,Request
from src.db.redis import check_in_redis

class TokenBearer(HTTPBearer):

    def __init__(self, *, bearerFormat = None, scheme_name = None, description = None, auto_error = True):
        super().__init__(bearerFormat=bearerFormat, scheme_name=scheme_name, description=description, auto_error=auto_error)

    async def __call__(self, request:Request):
        creds = await super().__call__(request)
        token = creds.credentials
        token_details = decode_token(token)
        if not token_details:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid or Expired token")
        if await check_in_redis(token_details['jti']):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Acessing logged out user")
        self.verify_token(token_details)
        return token_details

class AccessTokenBearer(TokenBearer):
    def verify_token(self,token_details:dict):
        if token_details['refresh'] is True:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Provide Access Token")
        
class RefreshTokenBearer(TokenBearer):
    def verify_token(self,token_details:dict):
        if token_details['refresh'] is False:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Provide Refresh Token")
        
