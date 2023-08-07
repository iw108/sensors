"""Definition of settings."""

from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    RABBITMQ_URI: str
    ATLAS_URI: AnyUrl

    DATABASE_NAME: str = "sensors"
    COLLECTION_NAME: str = "temperature"

    model_config = SettingsConfigDict(
        env_file='.env', 
        env_file_encoding='utf-8',
    )
