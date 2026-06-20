from sqlmodel import SQLModel,Field,Column
import uuid
from datetime import datetime,date
import sqlalchemy.dialects.postgresql as pg

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
    created_at: datetime = Field(default=datetime.now())