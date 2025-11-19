"""Conversation controller module."""

from dataclasses import dataclass

from app.dtos.conversation import CreateConversationRequest, CreateConversationResponse
from app.services.conversation import ConversationService


@dataclass
class ConversationController:
    """Controller to handle conversation requests."""

    conversation_service: ConversationService

    def create_conversation(
        self, payload: CreateConversationRequest, user_id: str
    ) -> CreateConversationResponse:
        """
        Create a new conversation.
        """
        return self.conversation_service.create_conversation(payload, user_id)
