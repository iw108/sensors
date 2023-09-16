"""Script for subscribing to MQTT topic via RabbitMQ."""

import asyncio
import logging
import logging.config
from pathlib import Path
from signal import SIGINT

import aio_pika
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync

from .message_handler import MessageHandler
from .settings import Settings

logging.config.fileConfig(
    Path(__file__).parent / "logging.conf",
    disable_existing_loggers=False,
)


LOGGER = logging.getLogger(__name__)


def _get_future(_loop: asyncio.AbstractEventLoop | None = None) -> asyncio.Future:
    future = asyncio.Future()

    loop = _loop or asyncio.get_event_loop()
    loop.add_signal_handler(SIGINT, lambda: future.set_result(True))

    return future


async def subscriber(
    *,
    _settings: Settings | None = None,
    _future: asyncio.Future | None = None,
):
    """Subscriber."""
    settings = _settings or Settings()

    connection = await aio_pika.connect_robust(settings.RABBITMQ_URI)

    influxdb_client = InfluxDBClientAsync(
        url=str(settings.INFLUXDB_URL),
        token=settings.INFLUXDB_TOKEN,
        org=settings.INFLUXDB_ORG,
    )

    async with connection, influxdb_client:
        message_handler = MessageHandler(
            write_api=influxdb_client.write_api(),
            bucket=settings.INFLUXDB_BUCKET,
        )

        channel = await connection.channel()

        mqtt_exchange = await channel.declare_exchange(
            name="amq.topic",
            type=aio_pika.ExchangeType.TOPIC,
            durable=True,
        )

        queue = await channel.declare_queue(name="mqtt")

        await queue.bind(
            exchange=mqtt_exchange,
            routing_key="sensors.temperature",
        )

        await queue.consume(message_handler)

        await (_future or _get_future())


if __name__ == "__main__":
    asyncio.run(subscriber())
