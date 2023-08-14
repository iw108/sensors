"""Definition of Data Transfer Object."""

from datetime import datetime, timezone

from pydantic import BaseModel, Field


class Metadata(BaseModel):
    sensor_id: int = Field(default=1, alias="sensorId")


class DataPoint(BaseModel):
    metadata: Metadata = Field(default_factory=Metadata)
    temperature: float
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
