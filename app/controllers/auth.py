"""Auth controller module."""

from dataclasses import dataclass

from app.dtos.auth import RegisterRequest, RegisterResponse
from app.services.auth import AuthService


@dataclass
class AuthController:
    """Controller to handle authentication requests."""

    auth_service: AuthService

    def register(self, payload: RegisterRequest) -> RegisterResponse:
        """
        Register a new user.
        """
        return self.auth_service.register_user(payload)
