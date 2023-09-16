"""Script for subscribing to MQTT topic via RabbitMQ."""

import asyncio
import logging
import logging.config
from contextlib import asynccontextmanager
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


def _get_cancelation_event(
    _loop: asyncio.AbstractEventLoop | None = None,
) -> asyncio.Future:
    event = asyncio.Event()

    loop = _loop or asyncio.get_event_loop()
    loop.add_signal_handler(SIGINT, event.set)

    return event


@asynccontextmanager
async def managed_message_handler(settings: Settings):
    influxdb_client = InfluxDBClientAsync(
        url=str(settings.INFLUXDB_URL),
        token=settings.INFLUXDB_TOKEN,
        org=settings.INFLUXDB_ORG,
    )

    async with influxdb_client:
        yield MessageHandler(
            write_api=influxdb_client.write_api(),
            bucket=settings.INFLUXDB_BUCKET,
        )


@asynccontextmanager
async def managed_queue(settings: Settings):
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URI)

    async with connection:
        channel = await connection.channel()

        mqtt_exchange = await channel.declare_exchange(
            name=settings.RABBITMQ_EXCHANGE_NAME,
            type=aio_pika.ExchangeType.TOPIC,
            durable=True,
        )

        queue = await channel.declare_queue(name=settings.RABBITMQ_QUEUE_NAME)

        await queue.bind(
            exchange=mqtt_exchange,
            routing_key=settings.RABBITMQ_ROUTING_KEY,
        )

        yield queue


async def main(
    *,
    _settings: Settings | None = None,
    _cancelation_event: asyncio.Event | None = None,
):
    settings = _settings or Settings()
    cancellation_event = _cancelation_event or _get_cancelation_event()

    async with (
        managed_queue(settings) as queue,
        managed_message_handler(settings) as message_handler,
    ):
        await queue.consume(message_handler)
        await cancellation_event.wait()


if __name__ == "__main__":
    asyncio.run(main())
