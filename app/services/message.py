"""Message service module."""

from dataclasses import dataclass

from fastapi import File, HTTPException, status

from app.agent.agent import Agent
from app.dtos.message import (
    GetMessagesResponse,
    MessageData,
    SendMessageRequest,
    SendMessageResponse,
)
from app.exceptions.bad_request import BadRequestException
from app.models.connection import Connection
from app.models.conversation import Conversation
from app.models.message import Message
from app.services.database import DatabaseService
from app.services.transcription import TranscriptionService
from app.utils.encrypt import Encrypt


@dataclass
class MessageService:
    """Service to handle messages."""

    async def send_message(
        self, payload: SendMessageRequest, user_id: str, conversation_id: str
    ) -> SendMessageResponse:
        """
        Send a message in a conversation.
        """
        conversation = await Conversation.get_or_none(id=conversation_id)
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found"
            )

        connection = await Connection.get_or_none(id=conversation.connection_id)
        if not connection:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Connection not found"
            )

        messages_ordered = (
            await Message.filter(conversation_id=conversation_id)
            .order_by("created_at")
            .all()
        )
        messages = [message.content for message in messages_ordered]

        await Message.create(
            content={"role": "user", "content": payload.message},
            user_id=user_id,
            conversation_id=conversation_id,
        )

        connection_url = Encrypt.decrypt(connection.encrypted_url)
        tables = DatabaseService.get_tables(connection_url)

        agent = Agent(
            model=conversation.model,
            connection_url=connection_url,
            messages=messages,
            context=conversation.context,
            tables=str(tables),
        )

        response = agent.run(message=payload.message)

        await Message.create(
            content={"role": "assistant", "content": response},
            user_id=user_id,
            conversation_id=conversation_id,
        )

        return SendMessageResponse(response=response)

    async def send_audio_message(
        self, file: File, user_id: str, conversation_id: str
    ) -> SendMessageResponse:
        """
        Send an audio message in a conversation.
        """
        conversation = await Conversation.get_or_none(id=conversation_id)
        if not conversation:
            raise BadRequestException("Conversation not found")

        connection = await Connection.get_or_none(id=conversation.connection_id)
        if not connection:
            raise BadRequestException("Connection not found")

        transcription_service = TranscriptionService(model="tiny")
        transcription_result = await transcription_service.transcribe(file)

        transcription = transcription_result["transcription"]

        messages = (
            await Message.filter(conversation_id=conversation_id)
            .order_by("-created_at")
            .all()
        )
        messages_content = [message.content for message in messages]

        content = {"role": "user", "content": transcription}
        await Message.create(
            content=content,
            user_id=user_id,
            conversation_id=conversation_id,
        )

        connection_url = Encrypt.decrypt(connection.encrypted_url)

        agent = Agent(
            model=conversation.model,
            connection_url=connection_url,
            messages=messages_content,
            context=conversation.context,
            tables=""
        )

        response = agent.run(message=transcription)

        content = {"role": "assistant", "content": response}
        await Message.create(
            content=content,
            user_id=user_id,
            conversation_id=conversation_id,
        )

        return SendMessageResponse(response=response)

    async def get_messages(self, conversation_id: str) -> GetMessagesResponse:
        """
        Retrieve messages from a conversation.
        """
        try:
            messages = (
                await Message.filter(conversation_id=conversation_id)
                .order_by("-created_at")
                .all()
            )
            data = [
                MessageData(
                    id=message.id,
                    content=message.content,
                )
                for message in messages
            ]

            return GetMessagesResponse(data=data)
        except Exception as e:
            raise e
