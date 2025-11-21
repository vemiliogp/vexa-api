"""Conversation service module."""

from dataclasses import dataclass

from app.dtos.conversation import (
    ConversationProfile,
    CreateConversationRequest,
    CreateConversationResponse,
)
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

            profile = ConversationProfile(
                id=conversation.id,
                title=conversation.title,
                context=conversation.context,
                connection_id=conversation.connection_id,
            )

            return CreateConversationResponse(data=profile)
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

    async def send_message(self, payload: dict, user_id: str, conversation_id: str):
        """
        Send a message within a conversation.
        """
        try:
            response = await self.message_service.send_message(
                payload, user_id, conversation_id
            )
            return response
        except Exception as e:
            raise e

    async def send_audio_message(self, file, user_id: str, conversation_id: str):
        """
        Send an audio message within a conversation.
        """
        try:
            response = await self.message_service.send_audio_message(
                file, user_id, conversation_id
            )
            return response
        except Exception as e:
            raise e

    async def get_messages(self, conversation_id: str):
        """
        Retrieve messages from a conversation.
        """
        try:
            messages = await self.message_service.get_messages(conversation_id)
            return messages
        except Exception as e:
            raise e
