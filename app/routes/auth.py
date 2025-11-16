"""Authentication routes module."""

from fastapi import APIRouter

from app.controllers.auth import AuthController
from app.dtos.auth import RegisterRequest, RegisterResponse, LoginRequest
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


@router.post("/login", response_model=str)
async def login(payload: LoginRequest):
    """
    Login an user endpoint.
    """
    session = await auth_controller.login(payload)
    return session
