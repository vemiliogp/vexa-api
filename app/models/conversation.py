"""Conversation model definition."""

from tortoise import fields
from tortoise.models import Model

from app.models.connection import Connection
from app.models.user import User


class Conversation(Model):
    """Conversation model representing a conversation in the system."""

    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=50, null=True)
    context = fields.TextField(null=True)

    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="conversations", on_delete=fields.CASCADE
    )
    connection: fields.ForeignKeyNullableRelation[Connection] = fields.ForeignKeyField(
        "models.Connection",
        related_name="conversations",
        null=True,
        on_delete=fields.SET_NULL,
    )

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
