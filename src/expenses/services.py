from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select,desc
from .models import expense_model
from .schemas import createexpense,updateexpense

class expense_service:

    async def get_all_expenses(self,session:AsyncSession):
        statement = select(expense_model).order_by(desc(expense_model.created_at))
        result = await session.execute(statement)
        expense = result.scalars().all()
        return expense if expense is not None else None
    
    async def get_expense(self,expense_id:str,session:AsyncSession):
        statement = select(expense_model).where(expense_model.id==expense_id)
        result = await session.execute(statement)
        expense = result.scalars().first()
        return expense if expense is not None else None
        
    async def create_expense(self, expense:createexpense,session:AsyncSession):
        expense_dict = expense.model_dump()
        new_expense = expense_model(**expense_dict)
        session.add(new_expense)
        await session.commit()
        return new_expense

    async def update_expense(self,expense_id:str,expense:updateexpense,session:AsyncSession):
        expense_model_item = await self.get_expense(expense_id,session)
        if expense_model_item is None:
            return None
        for k,v in expense.model_dump(exclude_unset=True).items():
            setattr(expense_model_item,k,v)
        await session.commit()
        return expense_model_item    

    async def delete_expense(self,expense_id:str,session:AsyncSession):
        expense_model_item = await self.get_expense(expense_id,session)
        if expense_model_item is None:
            return None
        await session.delete(expense_model_item)
        await session.commit()
        return "deleted"
        