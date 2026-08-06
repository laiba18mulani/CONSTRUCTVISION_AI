from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class JobKind(str, Enum):
    reconstruction = "RECONSTRUCTION"
    structural_fea = "STRUCTURAL_FEA"
    cfd = "CFD"
    flood = "FLOOD"


class AssetCreate(BaseModel):
    name: str = Field(min_length=3, max_length=120)
    location: str | None = Field(default=None, max_length=240)


class CaptureCreate(BaseModel):
    asset_id: UUID
    image_count: int = Field(ge=3, le=20_000)
    image_manifest_uri: str = Field(description="Immutable object-storage URI for the image package")
    calibrated: bool = False
    scale_reference_m: float | None = Field(default=None, gt=0)

    @field_validator("image_manifest_uri")
    @classmethod
    def require_object_uri(cls, value: str) -> str:
        if not value.startswith(("s3://", "gs://", "az://", "file://")):
            raise ValueError("image_manifest_uri must be an object-storage or file URI")
        return value


class TelemetrySample(BaseModel):
    sensor_id: str = Field(pattern=r"^[A-Za-z0-9_-]{3,80}$")
    measured_at: datetime
    metric: str = Field(pattern=r"^(strain|tilt|acceleration|displacement|temperature|humidity|water_level|wind_speed)$")
    value: float
    unit: str = Field(min_length=1, max_length=20)
    quality: str = Field(default="GOOD", pattern=r"^(GOOD|SUSPECT|BAD)$")
    metadata: dict[str, Any] = Field(default_factory=dict)


class TelemetryBatch(BaseModel):
    asset_id: UUID
    samples: list[TelemetrySample] = Field(min_length=1, max_length=10_000)


class AnalysisRequest(BaseModel):
    asset_id: UUID
    kind: JobKind
    model_revision: str = Field(min_length=3, max_length=128)
    inputs: dict[str, Any] = Field(default_factory=dict)

