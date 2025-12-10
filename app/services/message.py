"""Message service module."""

from dataclasses import dataclass

from litellm import completion

from app.agent.agent import Agent
from app.exceptions.bad_request import BadRequestException
from app.models.connection import Connection
from app.models.conversation import Conversation
from app.models.message import Message
from app.services.transcription import TranscriptionService
from app.utils.encrypt import Encrypt


@dataclass
class MessageService:
    """Service to handle messages."""

    async def send_message(self, payload, user_id: str, conversation_id: str):
        """
        Send a message in a conversation.
        """

        conversation = await Conversation.get_or_none(id=conversation_id)
        if not conversation:
            raise BadRequestException("Conversation not found")

        content = {"role": "user", "content": payload.get("message", "")}
        await Message.create(
            content=content,
            user_id=user_id,
            conversation_id=conversation_id,
        )

        connection = await Connection.get_or_none(id=conversation.connection_id)
        if not connection:
            raise BadRequestException("Connection not found")

        connection_url = Encrypt.decrypt(connection.encrypted_url)
        agent = Agent(model=conversation.model, connection_url=connection_url)

        response = agent.run(message=payload.get("message"))

        await Message.create(
            content=response.choices[0].message,
            user_id=user_id,
            conversation_id=conversation_id,
        )

        return {"result": response.choices[0].message.content}

    async def send_audio_message(self, file, user_id: str, conversation_id: str):
        """
        Send an audio message in a conversation.
        """

        transcription_service = TranscriptionService(model="tiny")
        transcription_result = await transcription_service.transcribe(file)

        print(transcription_result)

        content = {
            "role": "user",
            "content": f"Traduce al español y responde unicamente con la respuesta a la pregunta: {transcription_result['transcription']}",
        }

        await Message.create(
            content=content,
            user_id=user_id,
            conversation_id=conversation_id,
        )

        response = completion(
            model="ollama/qwen3:1.7b",
            messages=[
                content,
            ],
        )

        await Message.create(
            content=response.choices[0].message,
            user_id=user_id,
            conversation_id=conversation_id,
        )

        return {"result": response.choices[0].message.content}

    async def get_messages(self, conversation_id: str):
        """
        Retrieve messages from a conversation.
        """
        try:
            messages = await Message.filter(conversation_id=conversation_id).all()
            return messages
        except Exception as e:
            raise e
