"""DTOs for message endpoints."""

from pydantic import BaseModel, Field


class MessageData(BaseModel):
    """Shared message data dto."""

    id: int
    content: dict
    created_at: str


class GetMessagesResponse(BaseModel):
    """Response returned by the get messages endpoint."""

    data: list[MessageData] = Field(default_factory=list)
    message: str = "Messages retrieved successfully"


class SendMessageRequest(BaseModel):
    """Payload expected by the send message endpoint."""

    message: str = Field(min_length=1)


class SendMessageResponse(BaseModel):
    """Response returned by the send message endpoint."""

    response: str
    user_message: str
    message: str = "Message sent successfully"


class SendMessageAudioResponse(BaseModel):
    """Response returned by the send message audio endpoint."""

    url: str
    user_message: str
    message: str = "Message sent successfully"
