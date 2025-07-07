from authx import AuthX
from app.core.security import setup_authx
from fastapi import FastAPI

def init_auth(app: FastAPI) -> AuthX:
    return setup_authx(app)
