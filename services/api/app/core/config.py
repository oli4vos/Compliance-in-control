from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Aantoonbaar API"
    environment: str = "development"
    database_url: str = "sqlite:///./aantoonbaar-api.db"
    auto_seed_demo: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="AANTOONBAAR_",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
