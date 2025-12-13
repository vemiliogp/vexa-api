"""Conversation service module."""

from dataclasses import dataclass

from app.dtos.conversation import (
    ConversationData,
    CreateConversationRequest,
    CreateConversationResponse,
    GetConversationsResponse,
)
from app.dtos.message import (
    GetMessagesResponse,
    SendMessageRequest,
    SendMessageResponse,
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
                model=payload.model,
            )

            data = ConversationData(
                id=conversation.id,
                title=conversation.title,
                context=conversation.context,
                connection_id=conversation.connection_id,
                model=conversation.model,
            )

            return CreateConversationResponse(data=data)
        except Exception as e:
            raise e

    async def get_conversations(self, user_id: str) -> GetConversationsResponse:
        """
        Retrieve all conversations for a user.
        """
        try:
            conversations = await Conversation.filter(user_id=user_id).all()
            data = [
                ConversationData(
                    id=conversation.id,
                    title=conversation.title,
                    context=conversation.context,
                    model=conversation.model,
                )
                for conversation in conversations
            ]

            return GetConversationsResponse(data=data)
        except Exception as e:
            raise e

    async def send_message(
        self, payload: SendMessageRequest, user_id: str, conversation_id: str
    ) -> SendMessageResponse:
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

    async def get_messages(self, conversation_id: str) -> GetMessagesResponse:
        """
        Retrieve messages from a conversation.
        """
        try:
            messages = await self.message_service.get_messages(conversation_id)
            return messages
        except Exception as e:
            raise e
