from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    logger_config_path: str
    postgres_host: str
    postgres_port: str
    postgres_user: str
    postgres_db: str
    postgres_password: str
    secret_key: str
    access_token_timeout: int
    refresh_token_timeout: int
    crypt_algorithm: str
    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_settings():
    return Settings()
