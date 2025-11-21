"""Message service module."""

from dataclasses import dataclass

from litellm import completion

from app.models.message import Message
from app.services.transcription import TranscriptionService


@dataclass
class MessageService:
    """Service to handle messages."""

    async def send_message(self, payload, user_id: str, conversation_id: str):
        """
        Send a message in a conversation.
        """

        content = {"role": "user", "content": payload.get("message", "")}
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
