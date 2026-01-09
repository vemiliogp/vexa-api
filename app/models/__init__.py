"""Models registration."""

from app.models.connection import Connection
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.user import User
from app.models.insight import Insight

__all__ = ["User", "Connection", "Conversation", "Message", "Insight"]
