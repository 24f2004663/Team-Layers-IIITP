import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = Field("Life-GPS Operating System", validation_alias="APP_NAME")
    APP_ENV: str = Field("development", validation_alias="APP_ENV")
    DEBUG: bool = Field(True, validation_alias="DEBUG")
    API_VERSION: str = Field("1.0.0", validation_alias="API_VERSION")
    API_PREFIX: str = Field("/api/v1", validation_alias="API_PREFIX")
    TITLE: str = Field("Life-GPS API", validation_alias="TITLE")
    DESCRIPTION: str = Field("Agentic AI Operating System for Personal Growth", validation_alias="DESCRIPTION")

    # Database Settings
    DATABASE_URL: str = Field(
        "postgresql+asyncpg://postgres:postgres@localhost:5432/lifegps",
        validation_alias="DATABASE_URL"
    )
    SYNC_DATABASE_URL: str = Field(
        "postgresql://postgres:postgres@localhost:5432/lifegps",
        validation_alias="SYNC_DATABASE_URL"
    )

    # Google Gemini Settings
    GOOGLE_API_KEY: str = Field("mock_key", validation_alias="GOOGLE_API_KEY")
    GEMINI_MODEL: str = Field("gemini-1.5-pro", validation_alias="GEMINI_MODEL")

    # JWT Settings
    JWT_SECRET: str = Field("super_secret_jwt_token_signing_key_for_lifegps_development", validation_alias="JWT_SECRET")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60, validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(7, validation_alias="REFRESH_TOKEN_EXPIRE_DAYS")

    # Logging Settings
    LOG_LEVEL: str = Field("info", validation_alias="LOG_LEVEL")
    LOG_JSON_FORMAT: bool = Field(False, validation_alias="LOG_JSON_FORMAT")

    # Configuration for Pydantic Settings
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Instantiate settings
settings = Settings()
