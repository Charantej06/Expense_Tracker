from pydantic import BaseModel
from sqlmodel import Field
from datetime import datetime, date
from typing import Optional
import uuid


class create_user_schema(BaseModel):
    first_name: str 
    last_name: str 
    username: str = Field(max_length=15)
    email: str = Field(max_length=40)
    password_hash: str = Field(max_length=15)

class login_user_schema(BaseModel):
    email: str = Field(max_length=40)
    password_hash: str = Field(max_length=15)

class update_user_schema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] =None
    username: Optional[str] = Field(default=None, max_length=15)
    email: Optional[str] = Field(default=None, max_length=40)
    

class user_response_model(BaseModel):
    uid: uuid.UUID
    username: str
    first_name: str
    last_name: str 
    is_verified: bool
    email: str
    password_hash: str = Field(exclude=True)
    created_at: datetime

class verify_new_user_schema(BaseModel):
    email : str
    otp : str

class reset_password_schema(BaseModel):
    old_password : str
    new_password : str
    confirm_password :str

class forgetpassword_schema(BaseModel):
    email:str  

class verify_forgetpassword_schema(verify_new_user_schema):
    new_password : str
