"""DTOs for authentication endpoints."""

from pydantic import BaseModel, EmailStr, Field


class UserProfile(BaseModel):
    """Shared user profile dto."""

    id: int
    email: EmailStr = Field(max_length=50)
    full_name: str = Field(max_length=100, default="")


class LoginRequest(BaseModel):
    """Payload expected by the login endpoint."""

    email: EmailStr = Field(max_length=50)
    password: str = Field(min_length=8)


class LoginResponse(BaseModel):
    """Payload returned by the login endpoint."""

    data: UserProfile
    message: str = "User logged in successfully"


class RegisterRequest(BaseModel):
    """Payload expected by the registration endpoint."""

    email: EmailStr = Field(max_length=50)
    password: str = Field(min_length=8)
    full_name: str = Field(max_length=100, default="")


class RegisterResponse(BaseModel):
    """Payload returned by the registration endpoint."""

    data: UserProfile
    message: str = "User registered successfully"


class LogoutResponse(BaseModel):
    """Payload returned by the logout endpoint."""

    data: dict = Field(default_factory=dict)
    message: str = "User logged out successfully"
