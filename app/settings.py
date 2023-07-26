import os
import pathlib
from dotenv import load_dotenv
from pydantic import BaseSettings

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
load_dotenv()


class Settings(BaseSettings):
    BASE_DIR: pathlib.PurePath = BASE_DIR
    API_STR: str = "/api"
    USE_REDIS_CACHE: bool = True

    '''Database'''
    POSTGRES_HOST: str = os.environ.get("POSTGRES_HOST")
    POSTGRES_PORT: str = os.environ.get("POSTGRES_PORT")
    POSTGRES_DB: str = os.environ.get("POSTGRES_DB")
    POSTGRES_USER: str = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD")
    DB_STRING: str = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    '''Redis'''
    REDIS_HOST: str = os.environ.get("REDIS_HOST")
    REDIS_PORT: str = os.environ.get("REDIS_PORT")

    '''JSON Web Tokens'''
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 1800

    '''Hunter.io'''
    HUNTER_IO_KEY: str = os.environ.get("HUNTER_IO_KEY")


settings = Settings()

