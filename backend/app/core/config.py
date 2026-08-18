import os
from typing import List, Union
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Aivoa QMS Customer Complaint System"
    API_V1_STR: str = "/api"
    SECRET_KEY: str = "aivoa-secret-key-change-in-production"
    ENVIRONMENT: str = "development"

    # Database
    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/aivoa_qms"
    SQLITE_FALLBACK_URL: str = "sqlite:///./aivoa_qms.db"

    # Groq AI
    GROQ_API_KEY: str = ""
    LLM_MODEL: str = "groq/compound"
    LLM_TEMPERATURE: float = 0.1
    LLM_MAX_TOKENS: int = 1500

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
