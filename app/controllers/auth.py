"""Auth controller module."""

from dataclasses import dataclass

from app.dtos.auth import LoginRequest, RegisterRequest, RegisterResponse
from app.services.auth import AuthService


@dataclass
class AuthController:
    """Controller to handle authentication requests."""

    auth_service: AuthService

    async def login(self, payload: LoginRequest) -> str:
        """
        Login a user and return an authentication session.
        """
        return await self.auth_service.authenticate_user(payload)

    async def register(self, payload: RegisterRequest) -> RegisterResponse:
        """
        Register a new user.
        """
        return await self.auth_service.register_user(payload)
