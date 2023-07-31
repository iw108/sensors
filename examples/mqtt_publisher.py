"""Script for publishing messages to MQTT topic."""

from pathlib import Path

import paho.mqtt.publish as publish
from pydantic import Extra
from pydantic_settings import BaseSettings, SettingsConfigDict

from sensors.dto import DataPoint


class Settings(BaseSettings):
    MQTT_HOST: str = "localhost"
    MQTT_PORT: int = 1883

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / ".env",
        extra=Extra.ignore,
    )


def _get_message():
    return {"topic": "sensors/temperature", "payload": DataPoint().model_dump_json()}


def main(*, _settings: Settings | None = None):
    settings = _settings or Settings()

    publish.multiple(
        (_get_message() for _ in range(10)),
        hostname=settings.MQTT_HOST,
        port=settings.MQTT_PORT,
    )


if __name__ == "__main__":
    main()
