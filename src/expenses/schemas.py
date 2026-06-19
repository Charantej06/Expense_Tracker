from pydantic import BaseModel
import uuid
from datetime import date, datetime
from sqlmodel import Field
from typing import Optional

class createexpense(BaseModel):
    amount : int
    currency : str = Field(default="rupees")
    category : str
    expense_date : date

class updateexpense(BaseModel):
    amount : Optional[int] = None
    currency : Optional[str] = None
    category : Optional[str] = None
    expense_date : Optional[date] = None