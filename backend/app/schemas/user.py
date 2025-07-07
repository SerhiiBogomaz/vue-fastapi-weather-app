from pydantic import BaseModel, EmailStr, Field, ConfigDict
from fastapi import Form
from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(..., max_length=50, min_length=3)
    email: EmailStr

    @classmethod
    def as_form(
        cls,
        username: str = Form(..., max_length=50, min_length=3),
        email: EmailStr = Form(...)
    ):
        return cls(username=username, email=email)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=128)
    weather_api_key: str|None = None

    @classmethod
    def as_form(
        cls,
        username: str = Form(..., max_length=50, min_length=3),
        email: EmailStr = Form(...),
        password: str = Form(..., min_length=6, max_length=128),
        weather_api_key: str = Form(None, max_length=64),
    ):
        return cls(username=username, email=email, password=password, weather_api_key=weather_api_key)

class UserOut(UserBase):
    id: int
    created_at: datetime
    avatar_url: str | None = None
    is_active: bool = True
    weather_api_key: str | None = None

    model_config = ConfigDict(from_attributes=True)

class UserOutWithToken(UserOut):
    access_token: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    weather_api_key: str | None = Field(None, max_length = 64)
    delete_avatar: bool = False

    @classmethod
    def as_form(
        cls,
        weather_api_key: str = Form(None, max_length=64),
        delete_avatar: bool = Form(False)
    ):
        return cls(weather_api_key = weather_api_key, delete_avatar = delete_avatar)
