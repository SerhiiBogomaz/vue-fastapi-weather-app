from fastapi import Depends, Request, HTTPException, status
from authx import AuthX
from app.models.user import User

def get_auth(request: Request) -> AuthX:
    auth = getattr(request.app.state, 'auth', None)

    if auth is None:
        raise HTTPException(
            status_code=500,
            detail="Auth system not initialized. Call init_auth(app) first."
        )

    return auth
