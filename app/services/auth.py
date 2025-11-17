"""Auth service module."""

from dataclasses import dataclass

from app.dtos.auth import LoginRequest, LoginResponse, RegisterRequest, RegisterResponse
from app.models.user import User
from app.utils.password import Password


@dataclass
class AuthService:
    """Service to handle authentication."""

    async def authenticate_user(self, payload: LoginRequest) -> LoginResponse:
        """
        Authenticate a user and return an authentication session.
        """
        try:
            user = await User.get_or_none(email=payload.email)
            if not user or not Password.compare(payload.password, user.password_hash):
                raise ValueError("Invalid email or password")

            return LoginResponse(id=user.id, email=user.email, full_name=user.full_name)
        except Exception as e:
            raise e

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
