"""Health service module."""

from dataclasses import dataclass

from app.dtos.health import HealthResponse


@dataclass
class HealthService:
    """Service to check health status."""

    def check_health(self) -> HealthResponse:
        """
        Check the health status of the service.
        """
        return HealthResponse(status="OK")
