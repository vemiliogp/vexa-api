"""DTOs for connection endpoints."""

from pydantic import BaseModel, Field

from app.models.connection import EngineEnum


class ConnectionData(BaseModel):
    """Shared connection data dto."""

    id: int
    name: str
    description: str | None
    engine: EngineEnum


class CreateConnectionRequest(BaseModel):
    """Payload expected by the create connection endpoint."""

    name: str = Field(max_length=50)
    description: str | None = Field(default=None, max_length=100)
    engine: EngineEnum = Field(pattern=r"^(postgres)$")
    url: str = Field(min_length=1, pattern=r"^(postgres|postgresql):\/\/[^\s]+$")


class CreateConnectionResponse(BaseModel):
    """Response returned by the create connection endpoint."""

    data: ConnectionData
    message: str = "Connection created successfully"


class GetConnectionsResponse(BaseModel):
    """Response returned by the get connections endpoint."""

    data: list[ConnectionData] = Field(default_factory=list)
    message: str = "Connections retrieved successfully"


class CheckConnectionRequest(BaseModel):
    """Payload expected by the check connection endpoint."""

    url: str = Field(min_length=1, pattern=r"^(postgres|postgresql):\/\/[^\s]+$")


class CheckConnectionResponse(BaseModel):
    """Response returned by the check connection endpoint."""

    success: bool
    message: str = "Connection checked successfully"
