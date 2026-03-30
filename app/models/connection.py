"""Connection model definition."""

from enum import Enum

from app.models.user import User
from tortoise import fields
from tortoise.models import Model


class EngineEnum(str, Enum):
    """Database engine types."""

    POSTGRES = "postgres"


class Connection(Model):
    """Connection model representing a connection in the system."""

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    description = fields.CharField(max_length=100, null=True)

    engine = fields.CharEnumField(EngineEnum)
    encrypted_url = fields.TextField()

    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="connections", on_delete=fields.CASCADE
    )

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
