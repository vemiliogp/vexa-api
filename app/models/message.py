"""Message model definition."""

from app.models.conversation import Conversation
from tortoise import fields
from tortoise.models import Model


class Message(Model):
    """Message model representing a message in the system."""

    id = fields.IntField(pk=True)
    content = fields.JSONField()

    conversation: fields.ForeignKeyRelation[Conversation] = fields.ForeignKeyField(
        "models.Conversation", related_name="messages", on_delete=fields.CASCADE
    )

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
