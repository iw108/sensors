"""Script for subscribing to MQTT topic via RabbitMQ."""

import asyncio
from typing import Generator
from contextlib import contextmanager

import aio_pika
from aio_pika.message import AbstractIncomingMessage
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from .dto import DataPoint
from .settings import Settings


class MessageHandler:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def __call__(self, message: AbstractIncomingMessage):
        async with message.process():
            data_point = DataPoint.model_validate_json(message.body)
            await self.collection.insert_one(data_point.model_dump())


@contextmanager
def get_message_handler(settings: Settings) -> Generator[MessageHandler, None, None]:
    
    client = AsyncIOMotorClient(str(settings.ATLAS_URI))

    db = client.get_database(settings.DATABASE_NAME)

    yield MessageHandler(db.get_collection(settings.COLLECTION_NAME))

    client.close()


async def main(*, _settings: Settings | None = None):
    settings = _settings or Settings()

    with get_message_handler(settings) as message_handler:
        connection = await aio_pika.connect_robust(settings.RABBITMQ_URI)
        async with connection:
            channel = await connection.channel()

            temperature_exchange = await channel.declare_exchange(
                name="amq.topic",
                type=aio_pika.ExchangeType.TOPIC,
                durable=True,
            )

            queue = await channel.declare_queue(name="temperature_queue")

            await queue.bind(temperature_exchange, routing_key="sensors.temperature")

            async with queue.iterator() as iterator:
                async for message in iterator:
                    await message_handler(message)


if __name__ == "__main__":
    asyncio.run(main())
