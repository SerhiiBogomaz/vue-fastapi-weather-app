from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from typing import Literal

JWTAlgorithmType = Literal[
    'HS256', 'HS384', 'HS512',
    'RS256', 'RS384', 'RS512',
    'ES256', 'ES256K', 'ES384', 'ES512',
    'PS256', 'PS384', 'PS512'
]

class Settings(BaseSettings):
    JWT_SECRET_KEY: str = 'your_secret_123'
    JWT_ALGORITHM: JWTAlgorithmType = 'HS256'
    JWT_TOKEN_LOCATION: list = ["headers"]


    model_config = SettingsConfigDict(
        env_file = Path(__file__).parent.parent.parent / '.env',
        env_file_encoding = 'utf-8',
        extra='allow'
    )

settings = Settings()
