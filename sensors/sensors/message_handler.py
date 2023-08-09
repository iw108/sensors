from aio_pika.message import AbstractIncomingMessage
from influxdb_client.client.write_api_async import WriteApiAsync

from .dto import DataPoint


class MessageHandler:
    def __init__(self, write_api: WriteApiAsync, bucket: str):
        self.write_api = write_api
        self.bucket = bucket

    async def __call__(self, message: AbstractIncomingMessage):
        async with message.process():
            data_point = DataPoint.model_validate_json(message.body)

            data = {
                "measurement": "temperature",
                "tags": data_point.metadata.model_dump(),
                "fields": data_point.model_dump(exclude={"metadata", "timestamp"}),
                "time": data_point.timestamp.isoformat(),
            }

            await self.write_api.write(self.bucket, record=data)
