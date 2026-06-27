from sqlmodel import SQLModel,select
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import create_user_schema,update_user_schema
from .models import user_model
from .utils import hash_pass
from datetime import datetime
import uuid

class user_services:

    async def get_user_by_email(self,email:str,session:AsyncSession):
        statement = select(user_model).where(email==user_model.email)
        result = await session.execute(statement)
        user = result.scalars().first()
        return user if user is not None else None
    
    async def get_user_by_id(self,id:str,session:AsyncSession):
        statement = select(user_model).where(uuid.UUID(id)==user_model.uid)
        result = await session.execute(statement)
        user = result.scalars().first()
        return user if user is not None else None
    
    async def create_user(self,user:create_user_schema,session:AsyncSession):
        user_dict = user.model_dump()
        new_user = user_model(**user_dict)
        new_user.password_hash = hash_pass(user_dict['password_hash'])
        session.add(new_user)
        await session.commit()
        return new_user
    
    async def update_user(self,id:str,user:update_user_schema,session:AsyncSession):
        user_model_item = await self.get_user_by_id(id,session)
        if user_model_item is None:
            return None
        for k,v in user.model_dump(exclude_unset=True).items():
            setattr(user_model_item,k,v)
        setattr(user_model_item,"updated_at",datetime.now())   
        await session.commit()
        return user_model_item
    
    async def delete_user(self,id:str,session:AsyncSession):
        user = await self.get_user_by_id(id,session)
        if user is not None:
            await session.delete(user)
            await session.commit()
            return "deleted"
        return None
    