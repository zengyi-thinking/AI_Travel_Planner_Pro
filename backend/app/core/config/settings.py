"""
Application Settings Configuration

This module manages all application settings using Pydantic Settings.
It loads configuration from environment variables and .env files.
"""

from pydantic_settings import BaseSettings
from typing import List, Optional


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

    # Third-party Services
    WEATHER_API_KEY: Optional[str] = None
    FLIGHT_API_KEY: Optional[str] = None
    HOTEL_API_KEY: Optional[str] = None

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
    AI_MAX_TOKENS: int = 2000
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
    ALLOWED_ORIGINS: List[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create a global settings instance
settings = Settings()
