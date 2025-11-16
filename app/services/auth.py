"""Auth service module."""

from dataclasses import dataclass

from app.dtos.auth import RegisterRequest, RegisterResponse
from app.models.user import User
from app.utils.password import Password


@dataclass
class AuthService:
    """Service to handle authentication."""

    async def register_user(self, payload: RegisterRequest) -> RegisterResponse:
        """
        Register a new user.
        """
        try:
            user = await User.create(
                email=payload.email,
                full_name=payload.full_name,
                password_hash=Password.to_hash(payload.password),
            )

            return RegisterResponse(
                id=user.id,
                email=user.email,
                full_name=user.full_name,
            )
        except Exception as e:
            raise e
