"""Message service module."""

from dataclasses import dataclass

from fastapi import HTTPException, status
from fastapi.datastructures import UploadFile

from app.agent.agent import Agent
from app.agent.prompts.agent_prompt import get_default_agent_prompt
from app.dtos.message import (
    GetMessagesResponse,
    MessageData,
    SendMessageAudioResponse,
    SendMessageRequest,
    SendMessageResponse,
)
from app.models.connection import Connection
from app.models.conversation import Conversation
from app.models.message import Message
from app.services.database import DatabaseService
from app.services.llm import LLMService
from app.services.storage import StorageService
from app.services.transcription import TranscriptionService
from app.services.tts import TTSService
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
        try:
            conversation = await Conversation.get_or_none(id=conversation_id)
            if not conversation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found",
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

            system_prompt = get_default_agent_prompt(
                tables=str(tables),
                context=conversation.context,
            )

            agent = Agent(
                model=conversation.model,
                connection_url=connection_url,
                system_prompt=system_prompt,
                messages=messages,
            )

            response = agent.run(user_message=payload.message)

            await Message.create(
                content={"role": "assistant", "content": response},
                user_id=user_id,
                conversation_id=conversation_id,
            )

            if not conversation.title:
                title = await LLMService.generate(
                    "Genera un título conciso y descriptivo para la siguiente conversación, en menos de 50 caracteres y sin ningun tipo de formato, solo el titulo: "
                    + payload.message,
                    conversation.model,
                )
                conversation.title = title.capitalize()
                await conversation.save()

            return SendMessageResponse(response=response)
        except Exception as e:
            raise e

    async def send_audio_message(
        self, file: UploadFile, user_id: str, conversation_id: str
    ) -> SendMessageResponse:
        """
        Send an audio message in a conversation.
        """
        try:
            conversation = await Conversation.get_or_none(id=conversation_id)
            if not conversation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found",
                )

            connection = await Connection.get_or_none(id=conversation.connection_id)
            if not connection:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Connection not found"
                )

            transcription_service = TranscriptionService(model="tiny")
            transcription_result = await transcription_service.transcribe(file)
            transcription = transcription_result["transcription"]

            storage_service = StorageService()
            storage_service.save_file(
                bucket_name=f"conversation-{conversation_id}", file=file
            )

            messages_ordered = (
                await Message.filter(conversation_id=conversation_id)
                .order_by("created_at")
                .all()
            )
            messages = [message.content for message in messages_ordered]

            await Message.create(
                content={"role": "user", "content": transcription},
                user_id=user_id,
                conversation_id=conversation_id,
            )

            connection_url = Encrypt.decrypt(connection.encrypted_url)
            tables = DatabaseService.get_tables(connection_url)

            system_prompt = get_default_agent_prompt(
                tables=str(tables),
                context=conversation.context,
            )

            agent = Agent(
                model=conversation.model,
                connection_url=connection_url,
                system_prompt=system_prompt,
                messages=messages,
            )

            response = agent.run(user_message=transcription)

            tts_service = TTSService()
            audio_bytes = await tts_service.synthesize(response)
            url = storage_service.save_bytes(
                bucket_name=f"conversation-{conversation_id}",
                file_bytes=audio_bytes,
                file_extension="mp3",
            )

            await Message.create(
                content={"role": "assistant", "content": response},
                user_id=user_id,
                conversation_id=conversation_id,
            )

            return SendMessageAudioResponse(url=url)
        except Exception as e:
            raise e

    async def get_messages(self, conversation_id: str) -> GetMessagesResponse:
        """
        Retrieve messages from a conversation.
        """
        try:
            messages = (
                await Message.filter(conversation_id=conversation_id)
                .order_by("created_at")
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
