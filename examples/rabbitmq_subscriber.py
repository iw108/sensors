"""Script for subscribing to MQTT topic via RabbitMQ."""

import asyncio
from contextlib import contextmanager
from pathlib import Path

import aio_pika
from aio_pika.message import IncomingMessage
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

from sensors.dto import DataPoint


class Settings(BaseSettings):
    RABBITMQ_URI: str

    ATLAS_URI: AnyUrl
    DATABASE_NAME: str = "sensors"
    COLLECTION_NAME: str = "temperature"

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / ".env",
        extra="ignore",
    )


class MessageDelegator:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def __call__(self, message: IncomingMessage):
        async with message.process():
            data_point = DataPoint.model_validate_json(message.body)
            await self.collection.insert_one(data_point.model_dump())


@contextmanager
def get_message_delegator(settings: Settings):
    client = AsyncIOMotorClient(str(settings.ATLAS_URI))

    db = client.get_database(settings.DATABASE_NAME)

    yield MessageDelegator(db.get_collection(settings.COLLECTION_NAME))

    client.close()


async def main(*, _settings: Settings | None = None):
    settings = _settings or Settings()

    with get_message_delegator(settings) as message_delegator:
        connection = await aio_pika.connect_robust(settings.RABBITMQ_URI)
        async with connection:
            channel = await connection.channel()

            temperature_exchange = await channel.declare_exchange(
                name="amq.topic",
                type=aio_pika.ExchangeType.TOPIC,
                durable=True,
            )

            queue = await channel.declare_queue(name="temperature_queue")

            await queue.bind(temperature_exchange, routing_key="sensors.*")

            async with queue.iterator() as iterator:
                async for message in iterator:
                    await message_delegator(message)


if __name__ == "__main__":
    asyncio.run(main())
