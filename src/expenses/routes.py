from fastapi import APIRouter,Depends,HTTPException,status
from .schemas import createexpense,updateexpense
from src.db.main import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from .services import expense_service
from .models import expense_model

expense_service = expense_service()

expense_router = APIRouter()

@expense_router.get("/",response_model=list[expense_model],status_code=status.HTTP_200_OK)
async def get_all_expenses(session:AsyncSession = Depends(get_session)):
    all_expenses = await expense_service.get_all_expenses(session)
    if all_expenses is not None:
        return all_expenses
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

@expense_router.post("/create",response_model=expense_model,status_code=status.HTTP_201_CREATED)
async def create_expense(expense:createexpense,session:AsyncSession = Depends(get_session)):
    new_expense = await expense_service.create_expense(expense,session)
    return new_expense

@expense_router.patch("/update",response_model=expense_model,status_code=status.HTTP_202_ACCEPTED)
async def update_expense(expense_id:str,expense:updateexpense,session:AsyncSession = Depends(get_session)):
    expense_to_update = await expense_service.update_expense(expense_id,expense,session)
    if expense_to_update is not None:
        return expense_to_update
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    

@expense_router.delete("/delete",response_model=str,status_code=status.HTTP_200_OK)
async def delete_expense(expense_id:str,session:AsyncSession = Depends(get_session)):
    message = await expense_service.delete_expense(expense_id,session)
    if message is not None:
        return message
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)