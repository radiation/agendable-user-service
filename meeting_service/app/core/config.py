from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(from_attributes=True)
    TEST_DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"
    database_url: str = "sqlite:///./test.db"
    secret_key: str = "super_duper_secret_key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


settings = Settings()
