from fastapi import FastAPI
from src.expenses.routes import expense_router

app = FastAPI()

app.include_router(expense_router, prefix=f"/expenses")