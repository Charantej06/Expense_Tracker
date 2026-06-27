from sqlmodel import SQLModel,Field,Column,Relationship
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import date,datetime
from typing import Optional,TYPE_CHECKING
if TYPE_CHECKING:
    from src.auth.models import user_model


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
    user_uid: uuid.UUID = Field(foreign_key="User.uid",ondelete="CASCADE")
    user : "user_model" = Relationship(back_populates="expenses",)
    expense_date : date
    created_at : datetime = Field(default_factory=datetime.now)
    updated_at : datetime = Field(default_factory=datetime.now)
    