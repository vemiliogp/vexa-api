"""DTOs for authentication endpoints."""

from pydantic import BaseModel, ConfigDict, EmailStr


class UserProfile(BaseModel):
    """Shared user profile dto."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    full_name: str


class LoginRequest(BaseModel):
    """Payload expected by the login endpoint."""

    email: EmailStr
    password: str


class LoginResponse(UserProfile):
    """Payload returned by the login endpoint."""


class RegisterRequest(BaseModel):
    """Payload expected by the registration endpoint."""

    email: EmailStr
    password: str
    full_name: str


class RegisterResponse(UserProfile):
    """Payload returned by the registration endpoint."""

    message: str = "User registered successfully"
