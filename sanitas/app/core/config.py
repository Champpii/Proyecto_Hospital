import os
from typing import List
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = "Hospital Sanitas - Historial Médico"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "sanitas_dev_secret_key_2026")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./sanitas_dev.db"  # Soporta PostgreSQL o SQLite local si no hay servidor Postgres activo
    )
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "5"))
    MAX_FILE_SIZE_BYTES: int = MAX_FILE_SIZE_MB * 1024 * 1024
    ALLOWED_MIME_TYPES: List[str] = os.getenv(
        "ALLOWED_MIME_TYPES",
        "application/pdf,image/png,image/jpeg"
    ).split(",")
    SESSION_COOKIE_NAME: str = "sanitas_session"


settings = Settings()
