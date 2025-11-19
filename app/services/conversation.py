"""Conversation service module."""

from dataclasses import dataclass

from app.dtos.conversation import CreateConversationRequest, CreateConversationResponse
from app.models.conversation import Conversation
from app.services.message import MessageService


@dataclass
class ConversationService:
    """Service to handle conversations."""

    message_service: MessageService

    async def create_conversation(
        self, payload: CreateConversationRequest, user_id: str
    ) -> CreateConversationResponse:
        """
        Register a new conversation by user.
        """
        try:
            conversation = await Conversation.create(
                title=payload.title,
                context=payload.context,
                connection_id=payload.connection_id,
                user_id=user_id,
            )

            return CreateConversationResponse(
                id=conversation.id,
                title=conversation.title,
                context=conversation.context,
                connection_id=conversation.connection_id,
                user_id=conversation.user_id,
            )
        except Exception as e:
            raise e

    async def get_conversations(self, user_id: str):
        """
        Retrieve all conversations for a user.
        """
        try:
            conversations = await Conversation.filter(user_id=user_id).all()
            return conversations
        except Exception as e:
            raise e
