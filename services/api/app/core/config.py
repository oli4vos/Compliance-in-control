from functools import lru_cache

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Aantoonbaar API"
    environment: str = "development"
    database_url: str = "sqlite:///./aantoonbaar-api.db"
    auto_seed_demo: bool = False
    upload_dir: str = "storage/uploads"
    max_upload_bytes: int = 10 * 1024 * 1024
    openai_api_key: str | None = Field(
        default=None,
        validation_alias=AliasChoices("OPENAI_API_KEY", "AANTOONBAAR_OPENAI_API_KEY"),
    )
    openai_model: str = Field(
        default="gpt-6-astra",
        validation_alias=AliasChoices("OPENAI_MODEL", "AANTOONBAAR_OPENAI_MODEL"),
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="AANTOONBAAR_",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
