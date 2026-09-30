from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    SECRET_KEY: str
    DATABASE_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    LLM_MODEL: str = "llama3.2:3b"

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")


settings = Settings()

