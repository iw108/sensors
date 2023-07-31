from datetime import datetime, timezone

from pydantic import BaseModel, Field


class Metadata(BaseModel):
    sensor_id: int = 1


class DataPoint(BaseModel):
    metadata: Metadata = Field(default_factory=Metadata)
    temperature: int = 20
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
