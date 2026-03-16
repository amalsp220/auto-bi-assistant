import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = "gpt-4o-mini"
    MAX_FILE_SIZE_MB: int = 50
    MAX_SAMPLE_ROWS: int = 20
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "https://amalsp220.github.io",
        "https://*.vercel.app",
        "https://*.netlify.app",
    ]
    UPLOAD_DIR: str = "/tmp/uploads"

    class Config:
        env_file = ".env"

settings = Settings()
