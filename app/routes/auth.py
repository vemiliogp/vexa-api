"""Authentication routes module."""

from fastapi import APIRouter, Request

from app.controllers.auth import AuthController
from app.dtos.auth import (
    LoginRequest,
    LoginResponse,
    LogoutResponse,
    RegisterRequest,
    RegisterResponse,
)
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])
auth_controller = AuthController(AuthService())


@router.post("/register", response_model=RegisterResponse, status_code=201)
async def register(payload: RegisterRequest):
    """
    Register an user endpoint.
    """
    user = await auth_controller.register(payload)
    return user


@router.post("/login", response_model=LoginResponse)
async def login(payload: LoginRequest, request: Request):
    """
    Login an user endpoint.
    """
    user = await auth_controller.login(payload)
    request.session["user"] = user.model_dump()
    return user


@router.post("/logout", response_model=LogoutResponse)
async def logout(request: Request):
    """
    Logout an user endpoint.
    """
    user_data = request.session.get("user")
    if user_data:
        user_id = user_data.get("id")
        await auth_controller.logout(user_id)
        request.session.clear()
    return
