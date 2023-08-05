from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MQTT_HOST: str = "localhost"
    MQTT_PORT: int = 1883

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / ".env",
        extra="allow",
    )
