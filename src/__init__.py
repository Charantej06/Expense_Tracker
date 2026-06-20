from fastapi import FastAPI
from src.expenses.routes import expense_router
from src.auth.routes import auth_router

app = FastAPI()

app.include_router(expense_router, prefix=f"/expenses")
app.include_router(auth_router, prefix=f"/user")