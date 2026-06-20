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
    password_hash: str = Field(max_length=15,min_length=6)

class login_user_schema(BaseModel):
    email: str = Field(max_length=40)
    password_hash: str = Field(max_length=15,min_length=6)

class update_user_schema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] =None
    username: Optional[str] = Field(default=None, max_length=15)
    email: Optional[str] = Field(default=None, max_length=40)
    password_hash: Optional[str] = Field(default=None, max_length=15, min_length=6)

class user_response_model(BaseModel):
    uid: uuid.UUID
    username: str
    first_name: str
    last_name: str 
    is_verified: bool
    email: str
    password_hash: str = Field(exclude=True)
    created_at: datetime