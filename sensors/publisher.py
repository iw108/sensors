from contextlib import contextmanager
from typing import Generator
import os

import paho.mqtt.client as mqtt


@contextmanager
def get_client(
    *,
    _client: mqtt.Client | None = None,
) -> Generator[mqtt.Client, None, None]:
    client = _client or mqtt.Client()
    client.connect(
        os.getenv("MQTT_HOST", "127.0.0.1"),
        int(os.getenv("MQTT_PORT", "1883")),
    )

    client.loop_start()

    yield client

    client.loop_stop()
    client.disconnect()
