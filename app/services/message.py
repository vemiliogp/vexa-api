"""Message service module."""

from dataclasses import dataclass


@dataclass
class MessageService:
    """Service to handle messages."""

    def send_message(self, payload, user_id: str, conversation_id: str):
        """
        Send a message in a conversation.
        """
        # Placeholder implementation
        return {
            "message": "Message sent",
            "user_id": user_id,
            "payload": payload,
            "conversation_id": conversation_id,
        }
