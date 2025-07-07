from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.session import init_db, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await engine.dispose()
