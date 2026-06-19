from pydantic import BaseModel
import uuid
from datetime import date, datetime
from sqlmodel import Field

class createexpense(BaseModel):
    amount : int
    currency : str = Field(default="rupees")
    category : str
    expense_date : date

