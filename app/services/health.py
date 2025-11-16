"""Health service module."""

from dataclasses import dataclass


@dataclass
class HealthService:
    """Service to check health status."""

    def check_health(self) -> dict:
        """
        Check the health status of the service.
        """
        return {"status": "OK"}
