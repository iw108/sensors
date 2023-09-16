"""Definition of settings."""

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings required for subscriber."""

    RABBITMQ_URI: str
    RABBITMQ_EXCHANGE_NAME: str
    RABBITMQ_QUEUE_NAME: str = "mqtt"
    RABBITMQ_ROUTING_KEY: str = "sensors.temperature"

    INFLUXDB_BUCKET: str
    INFLUXDB_ORG: str
    INFLUXDB_TOKEN: str
    INFLUXDB_URL: AnyHttpUrl

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
