"""Conversation model definition."""

from tortoise import fields
from tortoise.models import Model

from app.models.user import User


class Conversation(Model):
    """Conversation model representing a conversation in the system."""

    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=50, unique=True)
    context = fields.TextField(null=True)

    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="conversations", on_delete=fields.CASCADE
    )

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
