"""Authentication routes module."""

from fastapi import APIRouter

from app.controllers.auth import AuthController
from app.dtos.auth import RegisterRequest, RegisterResponse
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])
auth_controller = AuthController(AuthService())


@router.post("/register", response_model=RegisterResponse, status_code=201)
def register(payload: RegisterRequest):
    """
    Register an user endpoint.
    """
    user = auth_controller.register(payload)
    return RegisterResponse.model_validate(user)
