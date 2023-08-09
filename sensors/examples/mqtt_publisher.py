"""Script for publishing messages to MQTT topic."""

import paho.mqtt.publish as publish
from config import Settings

from sensors.dto import DataPoint


def _get_message():
    return {
        "topic": "sensors/temperature",
        "payload": DataPoint(temperature=20).model_dump_json(),
    }


def main(*, _settings: Settings | None = None):
    settings = _settings or Settings()

    publish.multiple(
        (_get_message() for _ in range(2)),
        hostname=settings.MQTT_HOST,
        port=settings.MQTT_PORT,
    )


if __name__ == "__main__":
    main()
