from sqlmodel import SQLModel,Field,Column
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import date,datetime

class expense_model(SQLModel,table=True):
    __tablename__ = "expenses"

    id : uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            unique=True,
            nullable=False,
            default=uuid.uuid4,
            info={"description": "Unique identifier for the user account"},
        )
    )
    amount : int
    currency : str = Field(default="rupees")
    category : str
    expense_date : date
    created_at : datetime = Field(default=datetime.now())
    updated_at : datetime = Field(default=datetime.now())
    