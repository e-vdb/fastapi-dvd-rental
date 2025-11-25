"""Health check API endpoints."""

import time
from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, status
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app.api.deps import DatabaseSession
from app.core.config import get_settings
from app.core.logging_config import get_logger
from app.models.health import HealthStatus, ServiceCheck, Status

logger = get_logger(__name__)


router = APIRouter(
    prefix="/health",
    tags=["health"],
)

# Track application startup time
APP_START_TIME = datetime.now(tz=UTC)


def _check_database(db: DatabaseSession) -> ServiceCheck:
    """Check database connectivity."""
    start_time = time.time()

    try:
        result = db.execute(text("SELECT 1 as health_check"))
        row = result.fetchone()
        duration_ms = (time.time() - start_time) * 1000
        logger.info("Database connection successful: %s", row)

        return ServiceCheck(
            status=Status.HEALTHY,
            duration_ms=duration_ms,
        )

    except OperationalError as e:
        duration_ms = (time.time() - start_time) * 1000
        error = f"Database connection failed: {e!s}"
        logger.exception("database_health_check_failed")
        return ServiceCheck(
            status=Status.UNHEALTHY,
            duration_ms=duration_ms,
            error=error,
        )


async def perform_health_checks(db: DatabaseSession) -> dict[str, ServiceCheck]:
    """Perform all configured health checks."""
    return {
        "database": _check_database(db=db),
    }


@router.get("/", status_code=status.HTTP_200_OK)
async def health_summary(db: DatabaseSession) -> HealthStatus:
    """Comprehensive health check endpoint.

    Returns
    -------
    HealthStatus
        Overall status and individual service checks.

    """
    config = get_settings()

    # Perform all health checks
    checks = await perform_health_checks(db=db)

    # Determine overall status
    overall_status = Status.HEALTHY
    # If any check is unhealthy, overall status is unhealthy
    if checks and any(check.status == "unhealthy" for check in checks.values()):
        overall_status = Status.UNHEALTHY

    return HealthStatus(
        status=overall_status,
        version="1.0.0",
        environment="production" if not config.debug else "development",
        timestamp=datetime.now(UTC).isoformat(),
        uptime_seconds=(datetime.now(UTC) - APP_START_TIME).total_seconds(),
        checks=checks,
    )


@router.get("/live", status_code=status.HTTP_200_OK)
def liveness_check() -> dict[str, Any]:
    """Do a simple liveness check - just confirms the app is running.

    This endpoint should ALWAYS return 200 if the process is running.
    Used by Docker to determine if container should be restarted.

    Returns
    -------
        Simple status indicating the process is alive.

    """
    return {
        "status": "alive",
        "timestamp": datetime.now(tz=UTC).isoformat(),
    }
