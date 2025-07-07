from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status, Response, Request, Query
from pathlib import Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from authx import AuthX
import uuid
import httpx
from typing import Annotated

from app.models.user import User
from app.schemas.user import UserOut, UserCreate, UserOutWithToken, UserLogin, UserUpdate
from app.dependencies.database import get_db_session
from app.core.file_storage import file_storage
from app.core.security_utils import get_password_hash, verify_password
from app.dependencies.auth import get_auth
from app.core.logger import logger
from app.schemas.weather_response import WeatherResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserOutWithToken)
async def register_user(
    user_data: UserCreate = Depends(UserCreate.as_form),
    avatar: UploadFile | None = File(None),
    db: AsyncSession = Depends(get_db_session),
    auth: AuthX = Depends(get_auth)
):
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User email is already taken'
        )

    hashed_password = get_password_hash(user_data.password)

    avatar_url = None
    if avatar:
        try:
            file_storage.validate_file(avatar)
            file_suffix = Path(avatar.filename).suffix if avatar.filename else '.jpg'
            filename = f"user_{uuid.uuid4()}{file_suffix}"
            filepath = file_storage.AVATAR_DIR / filename
            with open(filepath, "wb") as buffer:
                buffer.write(await avatar.read())
            avatar_url = f"/static/avatars/{filename}"
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to save avatar: {str(e)}"
            )

    db_user = User(
        username = user_data.username,
        email = user_data.email,
        hashed_password = hashed_password,
        avatar_url = avatar_url,
        weather_api_key = user_data.weather_api_key,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    access_token = auth.create_access_token(uid = str(db_user.id))

    return UserOutWithToken(
        **UserOut.model_validate(db_user).model_dump(),
        access_token = access_token
    )

@router.post("/login", response_model=UserOutWithToken)
async def  login_user(
    user_data: UserLogin,
    db: AsyncSession = Depends(get_db_session),
    auth: AuthX = Depends(get_auth)
):
    result = await db.execute(select(User).where(User.email == user_data.email))
    db_user = result.scalar_one_or_none()

    if db_user is None or not verify_password(user_data.password, str(db_user.hashed_password)):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid email or password"
        )

    access_token = auth.create_access_token(uid = str(db_user.id))

    return UserOutWithToken(
        **UserOut.model_validate(db_user).model_dump(),
        access_token = access_token
    )

@router.delete("/me/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    request: Request,
    db: AsyncSession = Depends(get_db_session),
    auth: AuthX = Depends(get_auth)
):

    request_token = await auth.get_access_token_from_request(request)
    try:
        payload = auth.verify_token(
            request_token,
            verify_type = False,
            verify_fresh = False,
            verify_csrf = False
            )
    except Exception:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = 'Invalid or expired token'
        )
    user_id = int(payload.sub)
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = 'User not found'
        )

    await db.delete(user)
    await db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch("/me/update", response_model = UserOut)
async def update_user_me(
    user_data: Annotated[UserUpdate, Depends(UserUpdate.as_form)],
    request: Request,
    avatar: UploadFile | None = File(None),
    db: AsyncSession = Depends(get_db_session),
    auth: AuthX = Depends(get_auth)
):
    try:
        request_token = await auth.get_access_token_from_request(request)
        payload = auth.verify_token(request_token, verify_type=True)
        user_id = int(payload.sub)

        db_user = await db.get(User, user_id)
        if not db_user:
            logger.warning(f"User not found with ID: {user_id}")
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = 'User not found'
            )

        if user_data.weather_api_key not in (None, 'null'):
            db_user.weather_api_key = user_data.weather_api_key

        if user_data.delete_avatar:
            if db_user.avatar_url:
                avatar_path = Path(f".{db_user.avatar_url}")
                if avatar_path.exists():
                    avatar_path.unlink()
                db_user.avatar_url = None

        elif avatar:
            try:
                if db_user.avatar_url:
                    old_path = Path(f".{db_user.avatar_url}")
                    if old_path.exists():
                        old_path.unlink()

                file_storage.validate_file(avatar)
                file_suffix = Path(avatar.filename).suffix if avatar.filename else ".jpg"
                filename = f"user_{uuid.uuid4()}{file_suffix}"
                filepath = file_storage.AVATAR_DIR / filename

                with open(filepath, "wb") as f:
                    f.write(await avatar.read())

                db_user.avatar_url = f"/static/avatars/{filename}"

            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to save avatar: {str(e)}"
                )

        await db.commit()
        await db.refresh(db_user)
        logger.info(f"User {user_id} updated successfully")

        return UserOut.model_validate(db_user)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid user ID format: {str(e)}"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/me", response_model = UserOut)
async def get_current_user(
    request: Request,
    auth: AuthX = Depends(get_auth),
    db: AsyncSession = Depends(get_db_session)
):
    try:
        request_token = await auth.get_access_token_from_request(request)
        payload = auth.verify_token(
            request_token,
            verify_type=True,
            verify_fresh = False,
            verify_csrf = False
            )

        user_id = int(payload.sub)

        db_user = await db.get(User, user_id)
        if not db_user:
            logger.warning(f"User not found with ID: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found'
            )

        return UserOut.model_validate(db_user)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving current user: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

@router.get("/weather", response_model = WeatherResponse)
async def get_weather(
    city: str = Query(..., min_length = 2),
    api_key: str = Query(..., min_length = 32, max_length = 64),
):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "units": "metric",
        "appid": api_key
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=exc.response.json())
        except Exception:
            raise HTTPException(status_code=500, detail="Error while requesting the OpenWeather API")

    return response.json()
