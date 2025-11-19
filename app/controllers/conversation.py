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

    def get_conversations(self, user_id: str):
        """
        Retrieve all conversations for a user.
        """
        return self.conversation_service.get_conversations(user_id)

    def send_message(self, payload: dict, user_id: str):
        """
        Send a message in a conversation.
        """
        return self.conversation_service.message_service.send_message(payload, user_id)
