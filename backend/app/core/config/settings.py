"""
Application Settings Configuration

This module manages all application settings using Pydantic Settings.
It loads configuration from environment variables and .env files.
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
from pathlib import Path
import os

_ENV_PATH = Path(__file__).parent.parent.parent.parent / ".env"
if _ENV_PATH.exists():
    with _ENV_PATH.open("r", encoding="utf-8") as env_file:
        for line in env_file:
            if "=" in line and not line.strip().startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ[key] = value


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # Application Info
    APP_NAME: str = "WanderFlow"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4
    ALLOWED_HOSTS: List[str] = ["*"]

    # Database Configuration
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = "password"
    DB_NAME: str = "wanderflow_db"
    
    @property
    def DATABASE_URL(self) -> str:
        """Get async database URL"""
        return f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # JWT Configuration
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Redis Configuration
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None

    # AI Configuration
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL_NAME: str = "gpt-4-turbo-preview"
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    QA_API_KEY: Optional[str] = None
    ANTHROPIC_BASE_URL: Optional[str] = None
    ANTHROPIC_AUTH_TOKEN: Optional[str] = None
    ANTHROPIC_MODEL: Optional[str] = None
    ANTHROPIC_SMALL_FAST_MODEL: Optional[str] = None
    ANTHROPIC_DEFAULT_SONNET_MODEL: Optional[str] = None
    ANTHROPIC_DEFAULT_OPUS_MODEL: Optional[str] = None
    ANTHROPIC_DEFAULT_HAIKU_MODEL: Optional[str] = None
    API_TIMEOUT_MS: int = 60000

    # Vision API Configuration (OpenAI compatible)
    VISION_API_KEY: Optional[str] = None
    VISION_API_BASE_URL: Optional[str] = None
    VISION_MODEL: Optional[str] = None

    # Third-party Services
    WEATHER_API_KEY: Optional[str] = None
    WEATHER_API_ID: Optional[str] = None
    MAP_API_KEY: Optional[str] = None
    MAP_PROVIDER: Optional[str] = "baidu"  # baidu or amap
    MAP_SECRET_KEY: Optional[str] = None
    FLIGHT_API_KEY: Optional[str] = None
    HOTEL_API_KEY: Optional[str] = None

    # Claude Code Configuration
    CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC: Optional[str] = None

    # Email Configuration
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_TLS: bool = True

    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[str] = "logs/app.log"

    # AI Model Settings
    AI_TEMPERATURE: float = 0.7
    AI_MAX_TOKENS: int = 16000  # 澧炲姞token闄愬埗浠ユ敮鎸佸畬鏁磋绋嬬敓鎴?
    AI_TIMEOUT: int = 60

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000

    # File Upload Configuration
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: List[str] = [
        "image/jpeg",
        "image/png",
        "image/gif",
        "image/webp",
        "application/pdf"
    ]

    # Caching Configuration
    CACHE_TTL: int = 3600  # 1 hour
    CACHE_MAX_SIZE: int = 10000

    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = ["*", "http://localhost:3000", "http://localhost:3001", "http://localhost:3002", "http://localhost:3003", "http://localhost:5173"]

    class Config:
        env_file = str(Path(__file__).parent.parent.parent.parent / ".env")
        env_file_encoding = "utf-8"
        case_sensitive = True


# Create a global settings instance
settings = Settings()

