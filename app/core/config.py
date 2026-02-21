from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )

    app_name: str = Field(..., alias="APP_NAME")
    env: str = Field(..., alias="ENV")
    debug: bool = Field(..., alias="DEBUG")

    database_url: str = Field(..., alias="DATABASE_URL")

    jwt_secret: str = Field(..., alias="JWT_SECRET")
    jwt_algorithm: str = Field(..., alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(...,
                                             alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(...,
                                           alias="REFRESH_TOKEN_EXPIRE_DAYS")

    max_login_attempts: int = Field(..., alias="MAX_LOGIN_ATTEMPTS")
    account_lock_minutes: int = Field(..., alias="ACCOUNT_LOCK_MINUTES")


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
