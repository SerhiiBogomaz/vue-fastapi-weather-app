from fastapi import FastAPI
from authx import AuthX, AuthXConfig
from app.core.config import settings
from datetime import timedelta

if not settings.JWT_SECRET_KEY:
    raise ValueError('JWT_SECRET_KEY is not set! Check .env or enviroment variables.')

def setup_authx(app: FastAPI) -> AuthX:
    config = AuthXConfig (
        JWT_SECRET_KEY=settings.JWT_SECRET_KEY,
        JWT_ALGORITHM=settings.JWT_ALGORITHM,
        JWT_TOKEN_LOCATION=settings.JWT_TOKEN_LOCATION,
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=15),
    )
    auth = AuthX(config=config)
    auth.handle_errors(app)

    return auth
