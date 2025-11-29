"""DTOs for conversation endpoints."""

from pydantic import BaseModel, Field

from app.models.conversation import ModelEnum


class ConversationData(BaseModel):
    """Shared conversation data dto."""

    id: int
    title: str | None = None
    context: str | None = None
    model: ModelEnum
    connection_id: int | None = None


class CreateConversationRequest(BaseModel):
    """Payload expected by the create conversation endpoint."""

    title: str | None = Field(default=None, max_length=50)
    context: str | None = Field(default=None)
    model: ModelEnum = Field(pattern=r"^(deepseek-r1)$")
    connection_id: int | None = Field(default=None)


class CreateConversationResponse(BaseModel):
    """Response returned by the create conversation endpoint."""

    data: ConversationData
    message: str = "Conversation created successfully"
