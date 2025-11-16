"""User model definition."""

from tortoise import fields
from tortoise.models import Model


class User(Model):
    """User model representing a registered user in the system."""

    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=50, unique=True)
    password_hash = fields.CharField(max_length=128)
    full_name = fields.CharField(max_length=100, null=True)
