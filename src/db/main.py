from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
from src.config import config
from sqlmodel import SQLModel

engine = create_async_engine(url=config.DATABASE_URL,echo=True)

async_session= async_sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)

async def get_session():
    async with async_session() as session:
        yield session
