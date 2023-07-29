import json
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime
from typing import Generator

import board
from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin
from adafruit_dht import DHT22
from tenacity import retry, retry_if_exception_type


@contextmanager
def get_dht_device(pin: Pin = board.D22) -> Generator[DHT22, None, None]:
    dht_device = DHT22(pin)

    yield dht_device

    dht_device.exit()


@dataclass(frozen=True)
class Measurement:
    temperature: float | int | None
    humidity: float | int | None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def serialize(self) -> str:
        return json.dumps(self.__dict__)


@retry(retry=retry_if_exception_type(RuntimeError), wait=2)
def meausure(
    dht_device: DHT22,
    *,
    wait_inteval: int = 60,
) -> Generator[Measurement, None, None]:
    while True:
        yield Measurement(
            temperature=dht_device.temperature,
            humidity=dht_device.humidity,
        )
        time.sleep(wait_inteval)
