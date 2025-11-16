"""Utility functions for password management."""

from dataclasses import dataclass

from bcrypt import gensalt, hashpw


@dataclass
class Password:
    """Password utility class."""

    @staticmethod
    def to_hash(value: str) -> str:
        """
        Hash a password using bcrypt.
        """
        salt = gensalt()
        hashed = hashpw(value.encode("utf-8"), salt)
        return hashed.decode("utf-8")
