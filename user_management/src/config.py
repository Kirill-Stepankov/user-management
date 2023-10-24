from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    logger_config_path: str
    postgres_host: str
    postgres_host_test: str
    postgres_port: str
    postgres_db_test: str
    postgres_user: str
    postgres_db: str
    postgres_password: str
    secret_key: str
    access_token_timeout: int
    refresh_token_timeout: int
    crypt_algorithm: str
    localstack_endpoint_url: str
    s3_bucket_name: str
    aws_access_key_id: str
    aws_secret_access_key: str
    email_identity: str
    reset_pass_url: str

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_settings():
    return Settings()
