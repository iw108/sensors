"""Definition of RabbitMQ message handler."""

from aio_pika.message import AbstractIncomingMessage
from influxdb_client.client.write_api_async import WriteApiAsync

from .dto import DataPoint


class MessageHandler:
    """Class for processing RabbitMQ message."""

    def __init__(self, write_api: WriteApiAsync, bucket: str):
        """Initialise message handler.

        Args:
            write_api: Influxdb write api
            bucket: Name of bucket to write data to.

        """
        self.write_api = write_api
        self.bucket = bucket

    async def __call__(self, message: AbstractIncomingMessage):
        """Process message.

        Parse the message and propoagate resulting data point to Influxdb.

        Args:
            message: Incoming message.

        """
        async with message.process():
            data_point = DataPoint.model_validate_json(message.body)

            data = {
                "measurement": "temperature",
                "tags": data_point.metadata.model_dump(),
                "fields": data_point.model_dump(exclude={"metadata", "timestamp"}),
                "time": data_point.timestamp.isoformat(),
            }

            await self.write_api.write(self.bucket, record=data)
