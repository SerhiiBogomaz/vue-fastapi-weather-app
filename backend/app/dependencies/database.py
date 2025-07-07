from app.db.session import AsyncSessionLocal
from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db() -> AsyncGenerator:
    async with AsyncSessionLocal() as session:
        yield session

async def get_db_session(db: AsyncSession = Depends(get_db)) -> AsyncSession:
    return db
