"""Auth controller module."""

from dataclasses import dataclass

from app.dtos.auth import (
    LoginRequest,
    LoginResponse,
    LogoutResponse,
    RegisterRequest,
    RegisterResponse,
)
from app.services.auth import AuthService


@dataclass
class AuthController:
    """Controller to handle authentication requests."""

    auth_service: AuthService

    async def login(self, payload: LoginRequest) -> LoginResponse:
        """
        Login a user and return an authentication session.
        """
        try:
            return await self.auth_service.authenticate_user(payload)
        except Exception as e:
            raise e

    async def register(self, payload: RegisterRequest) -> RegisterResponse:
        """
        Register a new user.
        """
        try:
            return await self.auth_service.register_user(payload)
        except Exception as e:
            raise e

    async def logout(self, user_id: str) -> LogoutResponse:
        """
        Logout a user by invalidating their session.
        """
        try:
            return await self.auth_service.logout_user(user_id)
        except Exception as e:
            raise e
