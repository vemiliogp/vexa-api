"""DTOs for message endpoints."""

from pydantic import BaseModel, Field


class MessageData(BaseModel):
    """Shared message data dto."""

    id: int
    content: dict


class GetMessagesResponse(BaseModel):
    """Response returned by the get messages endpoint."""

    data: list[MessageData] = Field(default_factory=list)
    message: str = "Messages retrieved successfully"
