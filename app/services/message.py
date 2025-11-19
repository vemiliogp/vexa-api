"""Message service module."""

from dataclasses import dataclass

from litellm import completion

from app.models.message import Message


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

        # Placeholder implementation
        return {
            "message": "Message sent",
            "user_id": user_id,
            "payload": payload,
            "response": response,
            "conversation_id": conversation_id,
        }
