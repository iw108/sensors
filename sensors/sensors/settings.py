"""Definition of settings."""

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings required for subscriber."""

    RABBITMQ_URI: str
    RABBITMQ_MQTT_EXCHANGE: str = "mqtt"

    INFLUXDB_BUCKET: str
    INFLUXDB_ORG: str
    INFLUXDB_TOKEN: str
    INFLUXDB_URL: AnyHttpUrl

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
