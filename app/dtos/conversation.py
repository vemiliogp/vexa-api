"""DTOs for conversation endpoints."""

from app.models.conversation import ModelEnum
from pydantic import BaseModel, Field


class ConversationData(BaseModel):
    """Shared conversation data dto."""

    id: int
    title: str | None = None
    context: str | None = None
    model: ModelEnum
    connection_id: int | None = None
    created_at: str


class CreateConversationRequest(BaseModel):
    """Payload expected by the create conversation endpoint."""

    title: str | None = Field(default=None, max_length=50)
    context: str | None = Field(default=None)
    model: ModelEnum = Field(pattern=r"^(deepseek/r1|openai/gpt-5|openai/gpt-oss|ollama/deepseek-r1:14b)$")
    connection_id: int | None = Field(default=None)


class CreateConversationResponse(BaseModel):
    """Response returned by the create conversation endpoint."""

    data: ConversationData
    message: str = "Conversation created successfully"


class GetConversationsResponse(BaseModel):
    """Response returned by the get conversations endpoint."""

    data: list[ConversationData] = Field(default_factory=list)
    message: str = "Conversations retrieved successfully"
