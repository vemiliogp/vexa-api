"""DTOs for conversation endpoints."""

from pydantic import BaseModel


class CreateConversationRequest(BaseModel):
    """Payload expected by the create conversation endpoint."""

    title: str | None = None
    context: str | None = None
    connection_id: int | None = None


class CreateConversationResponse(BaseModel):
    """Response returned by the create conversation endpoint."""

    id: int
    title: str | None = None
    context: str | None = None
    connection_id: int | None = None
    created_at: str
    updated_at: str
