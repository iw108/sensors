from contextlib import contextmanager
from typing import Generator

import paho.mqtt.client as mqtt


@contextmanager
def get_client(
    *, _client: mqtt.Client | None = None
) -> Generator[mqtt.Client, None, None]:
    client = _client or mqtt.Client()
    client.connect("127.0.0.1", 1883, 60)

    client.loop_start()

    yield client

    client.loop_stop()
    client.disconnect()
