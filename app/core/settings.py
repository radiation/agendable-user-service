import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from the .env file
load_dotenv()


class Settings(BaseSettings):
    # Secret key for token generation
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default_secret_key")
    print("Settings SECRET_KEY: ", SECRET_KEY)

    # DB Connection
    DB_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))
    DB_USER: str = os.getenv("POSTGRES_USER", "user")
    DB_PASS: str = os.getenv("POSTGRES_PASSWORD", "password")
    DB_NAME: str = os.getenv("POSTGRES_DB", "user_db")
    DB_URL: str = os.getenv(
        "USER_DB_URL",
        "postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PORT}@postgres/${DB_NAME}",
    )

    # Redis
    REDIS_HOST: str = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB: int = int(os.getenv("REDIS_DB", 0))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")


settings = Settings()
