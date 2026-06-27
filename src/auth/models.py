from sqlmodel import SQLModel,Field,Column,Relationship
import uuid
from datetime import datetime,date
import sqlalchemy.dialects.postgresql as pg
from typing import Optional,TYPE_CHECKING
if TYPE_CHECKING:
    from src.expenses.models import expense_model

class user_model(SQLModel,table=True):
    __tablename__ = "User"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            unique=True,
            nullable=False,
            default=uuid.uuid4,
            info={"description": "Unique identifier for the user account"},
        )
    )

    username: str
    first_name: str = Field(nullable=True)
    last_name: str = Field(nullable=True)
    is_verified: bool = False
    email: str
    password_hash: str
    expenses : list["expense_model"] = Relationship(back_populates="user",
                                                    sa_relationship_kwargs={
                                                        "cascade":"all, delete-orphan",
                                                        "passive_deletes":True
                                                    })
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at : datetime = Field(default_factory=datetime.now)