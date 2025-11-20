"""DTOs for connection endpoints."""

from pydantic import BaseModel, Field


class ConnectionProfile(BaseModel):
    """Shared connection profile dto."""

    id: int
    name: str
    description: str | None
    engine: str
    url: str


class CreateConnectionRequest(BaseModel):
    """Payload expected by the create connection endpoint."""

    name: str = Field(max_length=50)
    description: str | None = Field(default=None, max_length=100)
    engine: str = Field(pattern="^(postgres|mysql|sqlite)$")
    url: str = Field(min_length=1)


class CreateConnectionResponse(BaseModel):
    """Response returned by the create connection endpoint."""

    data: ConnectionProfile
    message: str = "Connection created successfully"
