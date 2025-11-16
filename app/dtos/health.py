"""DTOs for health endpoints."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Payload returned by the health check."""

    status: str
