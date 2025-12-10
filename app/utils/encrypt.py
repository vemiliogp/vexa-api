"""Utility functions for encryption management."""

from dataclasses import dataclass
from os import getenv

from cryptography.fernet import Fernet


@dataclass
class Encrypt:
    """Encryption utility class."""

    @staticmethod
    def encrypt(value: str) -> str:
        """
        Encrypt a value using symmetric encryption.
        """
        key = getenv("ENCRYPT_SECRET")
        encrypted = Fernet(key).encrypt(value.encode())
        return encrypted.decode()

    @staticmethod
    def decrypt(value: str) -> None:
        """
        Decrypt a value using symmetric encryption.
        """
        key = getenv("ENCRYPT_SECRET")
        fernet = Fernet(key)
        decrypted_bytes = fernet.decrypt(value.encode())
        return decrypted_bytes.decode()
