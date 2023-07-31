"""Script for subscribing to MQTT topic."""

from pathlib import Path

from paho.mqtt.client import Client, MQTTMessage
from pydantic import Extra
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MQQT_HOST: str = "localhost"
    MQTT_PORT: int = 1883

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / ".env",
        extra=Extra.ignore,
    )


def _on_connect(client: Client, userdata, flags, rc: int):
    if rc == 0:
        client.subscribe("sensors/temperature")


def _on_message(client: Client, userdata, msg: MQTTMessage):
    print(f"{msg.topic}: {msg.payload}")


def main(*, _settings: Settings | None = None):
    settings = _settings or Settings()

    client = Client()
    client.on_connect = _on_connect
    client.on_message = _on_message

    client.connect(settings.MQQT_HOST, settings.MQTT_PORT)

    client.loop_forever()


if __name__ == "__main__":
    main()
