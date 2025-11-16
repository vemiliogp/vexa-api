"""Auth service module."""

from dataclasses import dataclass

from app.dtos.auth import RegisterRequest, RegisterResponse
from app.models.user import User


@dataclass
class AuthService:
    """Service to handle authentication."""

    async def register_user(self, payload: RegisterRequest) -> RegisterResponse:
        """
        Register a new user.
        """

        user = await User.create(
            email=payload.email,
            full_name=payload.full_name,
            password_hash=payload.password,
        )

        return RegisterResponse(
            email=user.email,
            full_name=user.full_name,
        )
