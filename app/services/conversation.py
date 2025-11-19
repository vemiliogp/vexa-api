"""Conversation service module."""

from dataclasses import dataclass

from app.dtos.conversation import CreateConversationRequest, CreateConversationResponse
from app.models.conversation import Conversation


@dataclass
class ConversationService:
    """Service to handle conversations."""

    async def create_conversation(
        self, payload: CreateConversationRequest
    ) -> CreateConversationResponse:
        """
        Register a new conversation by user.
        """
        try:
            conversation = await Conversation.create(
                title=payload.title,
                context=payload.context,
                connection_id=payload.connection_id,
                user_id=1,
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
