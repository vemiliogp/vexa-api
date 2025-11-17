"""DTOs for connection endpoints."""

from pydantic import BaseModel


class CreateConnectionRequest(BaseModel):
    """Payload expected by the create connection endpoint."""

    name: str
    description: str | None
    engine: str
    url: str


class CreateConnectionResponse(BaseModel):
    """Response returned by the create connection endpoint."""

    id: int
    name: str
    description: str | None
    engine: str
    url: str
