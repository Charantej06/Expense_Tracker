from fastapi import APIRouter

expense_router = APIRouter()

@expense_router.get("/")
def get_all_expenses():
    return f"Hello charan"

@expense_router.get("/create")
def create_expense():
    pass

@expense_router.get("/update")
def update_expense():
    pass

@expense_router.get("/delete")
def delete_expense():
    pass