"""Conversation controller module."""

from dataclasses import dataclass

from fastapi import File

from app.dtos.conversation import (
    CreateConversationRequest,
    CreateConversationResponse,
    GetConversationsResponse,
)
from app.dtos.message import (
    GetMessagesResponse,
    SendMessageRequest,
    SendMessageResponse,
)
from app.services.conversation import ConversationService


@dataclass
class ConversationController:
    """Controller to handle conversation requests."""

    conversation_service: ConversationService

    async def create_conversation(
        self, payload: CreateConversationRequest, user_id: str
    ) -> CreateConversationResponse:
        """
        Create a new conversation.
        """
        try:
            return await self.conversation_service.create_conversation(
                payload=payload, user_id=user_id
            )
        except Exception as e:
            raise e

    async def get_conversations(self, user_id: str) -> GetConversationsResponse:
        """
        Retrieve all conversations for a user.
        """
        try:
            return await self.conversation_service.get_conversations(user_id=user_id)
        except Exception as e:
            raise e

    async def send_message(
        self, payload: SendMessageRequest, user_id: str, conversation_id: str
    ) -> SendMessageResponse:
        """
        Send a text message in a conversation.
        """
        try:
            return await self.conversation_service.message_service.send_message(
                payload=payload, user_id=user_id, conversation_id=conversation_id
            )
        except Exception as e:
            raise e

    async def send_audio_message(self, file: File, user_id: str, conversation_id: str):
        """
        Send an audio message in a conversation.
        """
        try:
            return await self.conversation_service.message_service.send_audio_message(
                file=file, user_id=user_id, conversation_id=conversation_id
            )
        except Exception as e:
            raise e

    async def get_messages(self, conversation_id: str) -> GetMessagesResponse:
        """
        Retrieve messages from a conversation.
        """
        try:
            return await self.conversation_service.message_service.get_messages(
                conversation_id=conversation_id
            )
        except Exception as e:
            raise e
