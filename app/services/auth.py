"""Auth service module."""

from dataclasses import dataclass

from app.dtos.auth import RegisterRequest, RegisterResponse


@dataclass
class AuthService:
    """Service to handle authentication."""

    def register_user(self, payload: RegisterRequest) -> RegisterResponse:
        """
        Register a new user.
        """

        return RegisterResponse(
            email=payload.email,
            full_name=payload.full_name,
        )
