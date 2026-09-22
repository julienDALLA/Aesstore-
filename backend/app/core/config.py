"""
Application configuration using Pydantic Settings.
Environment variables are loaded from .env file.
"""

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    
    # Application
    APP_NAME: str = "Aesstore API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "B2B E-commerce Platform Backend"
    DEBUG: bool = False
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://user:password@db:5432/aesstore",
        validation_alias="DATABASE_URL"
    )
    DATABASE_TEST_URL: str = "sqlite+aiosqlite:///:memory:"
    
    # Security
    SECRET_KEY: str = Field(
        default="change-me-in-production-use-secrets-generate",
        validation_alias="SECRET_KEY"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    CORS_ORIGINS_REGEX: str = r"^https:\/\/.*\.aesstore\.com$"
    CORS_HEADERS: list[str] = ["*"]
    CORS_METHODS: list[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    
    # Rate Limiting
    RATE_LIMIT: int = 100
    RATE_LIMIT_PER: str = "minute"
    
    # File Upload
    MAX_FILE_SIZE_MB: int = 10
    UPLOAD_DIR: str = "uploads"
    ALLOWED_FILE_TYPES: list[str] = [".jpg", ".jpeg", ".png", ".pdf", ".docx"]
    
    # Email (for password reset, notifications)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = "noreply@aesstore.com"
    SMTP_FROM_NAME: str = "Aesstore"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: str = "logs/app.log"
    
    # Pagination
    DEFAULT_PAGE: int = 1
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def validate_database_url(cls, v: Optional[str]) -> str:
        if not v:
            raise ValueError("DATABASE_URL is required")
        return v
    
    @field_validator("SECRET_KEY", mode="before")
    @classmethod
    def validate_secret_key(cls, v: Optional[str]) -> str:
        if not v or v == "change-me-in-production-use-secrets-generate":
            import secrets
            v = secrets.token_urlsafe(32)
        return v
    
    @property
    def is_production(self) -> bool:
        return not self.DEBUG
    
    @property
    def is_testing(self) -> bool:
        return os.getenv("TESTING", "false").lower() == "true"


# Create settings instance
settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs("logs", exist_ok=True)
