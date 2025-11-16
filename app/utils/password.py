"""Utility functions for password management."""

from dataclasses import dataclass

from bcrypt import checkpw, gensalt, hashpw


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

    @staticmethod
    def compare(supplied_password: str, stored_password: str) -> bool:
        """
        Compare a stored hashed password with a supplied password.
        """
        return checkpw(supplied_password.encode(), stored_password.encode())
