import os
from dotenv import load_dotenv
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import (List,
                    ClassVar)


load_dotenv()


class Settings(BaseSettings):
    PROJECT_ROOT: ClassVar[Path] = Path(__file__).resolve().parents[2]

    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    ALLOW_CREDENTIALS: bool = True
    ALLOW_METHODS: List[str] = ["*"]
    ALLOW_HEADERS: List[str] = ["*"]
    API_KEY: ClassVar[Path] = os.getenv('API_KEY')
    API_KEY_NAME: ClassVar[Path] = os.getenv('API_KEY_NAME')
    SQLALCHEMY_DATABASE_URL: ClassVar[str] = "sqlite:///./database/vitaFiesta.db" 


settings = Settings()
