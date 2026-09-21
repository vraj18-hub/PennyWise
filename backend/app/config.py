from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Path to the main PennyWise folder (config.py is 3 levels down from it)
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    SECRET_KEY: str
    LLM_API_KEY: str
    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")


settings = Settings()