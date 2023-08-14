"""Definition of Data Transfer Object."""

from datetime import datetime, timezone

from pydantic import BaseModel, Field


class Metadata(BaseModel):
    """Metadata relating to measurement."""

    sensor_id: int = Field(default=1, alias="sensorId")


class DataPoint(BaseModel):
    """Data point corresponding to DH22 measurement."""

    metadata: Metadata = Field(default_factory=Metadata)
    temperature: float
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
