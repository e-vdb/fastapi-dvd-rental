"""Models for health router endpoints."""

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict


class Status(str, Enum):
    """Enum for the health status."""

    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"


class HealthStatus(BaseModel):
    """Health check response model."""

    model_config = ConfigDict(
        use_enum_values=True,
    )

    status: Status
    timestamp: str
    uptime_seconds: float
    version: str
    environment: str
    checks: dict[str, Any]


class ServiceCheck(BaseModel):
    """Individual service check result."""

    status: Status
    duration_ms: float
    error: str | None = None
