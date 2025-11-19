"""Health controller module."""

from dataclasses import dataclass

from app.dtos.health import HealthResponse
from app.services.health import HealthService


@dataclass
class HealthController:
    """Controller to handle health check requests."""

    health_service: HealthService

    def get_health(self) -> HealthResponse:
        """
        Get the API health status.
        """
        return self.health_service.check_health()
