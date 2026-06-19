from fastapi import APIRouter,Depends
from .schemas import createexpense
from src.db.main import get_session
from sqlalchemy.ext.asyncio import AsyncSession

expense_router = APIRouter()

@expense_router.get("/")
async def get_all_expenses(session:AsyncSession = Depends(get_session)):
    return f"Hello charan"

@expense_router.post("/create",response_model=createexpense)
async def create_expense(expense:createexpense,session:AsyncSession = Depends(get_session)):
    return expense

@expense_router.put("/update",response_model=createexpense)
async def update_expense(expense:createexpense,session:AsyncSession = Depends(get_session)):
    return expense

@expense_router.delete("/delete",response_model=str)
async def delete_expense(expense_id:str,session:AsyncSession = Depends(get_session)):
    return expense_id