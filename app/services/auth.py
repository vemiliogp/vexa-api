"""Auth service module."""

from dataclasses import dataclass

from app.dtos.auth import (
    LoginRequest,
    LoginResponse,
    LogoutResponse,
    RegisterRequest,
    RegisterResponse,
    UserProfile,
)
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

            profile = UserProfile(
                id=user.id, email=user.email, full_name=user.full_name
            )
            return LoginResponse(data=profile)
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

            profile = UserProfile(
                id=user.id, email=user.email, full_name=user.full_name
            )
            return RegisterResponse(data=profile)
        except Exception as e:
            raise e

    async def logout_user(self, user_id: str) -> LogoutResponse:
        """
        Logout a user by invalidating their session.
        """
        try:
            user = await User.get_or_none(id=user_id)
            if not user:
                raise ValueError("User not found")
            return LogoutResponse()
        except Exception as e:
            raise e
