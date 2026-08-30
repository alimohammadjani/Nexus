"""Application configuration loaded from environment variables."""

from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central settings object for the DevHub backend."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # General
    app_name: str = "DevHub"
    debug: bool = True
    api_prefix: str = "/api/v1"
    allowed_origins: str = "http://localhost:5173,http://localhost:3000"
    frontend_url: str = "http://localhost:5173"

    # Database
    database_url: str = "sqlite:///./devhub.db"

    # Redis / tasks
    redis_url: str = "redis://localhost:6379"

    # Demo data
    seed_demo: bool = True

    # Security
    secret_key: str = "change-me-in-production-please-use-a-long-random-value"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # Optional integrations
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_bucket_name: str = "devhub-files"
    aws_region: str = "us-east-1"
    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""
    resend_api_key: str = ""
    sentry_dsn: str = ""

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def _split_origins(cls, value: str) -> str:
        if isinstance(value, (list, tuple)):
            return ",".join(value)
        return value

    @property
    def origins(self) -> list[str]:
        """Return allowed origins as a clean list."""
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
