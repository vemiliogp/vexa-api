"""DTOs for conversation endpoints."""

from pydantic import BaseModel, Field


class ConversationProfile(BaseModel):
    """Shared conversation profile dto."""

    id: int
    title: str | None = None
    context: str | None = None
    connection_id: int | None = None


class CreateConversationRequest(BaseModel):
    """Payload expected by the create conversation endpoint."""

    title: str | None = Field(default=None, max_length=50)
    context: str | None = Field(default=None)
    connection_id: int | None = Field(default=None)


class CreateConversationResponse(BaseModel):
    """Response returned by the create conversation endpoint."""

    data: ConversationProfile
    message: str = "Conversation created successfully"
