"""Health routes module."""

from app.controllers.health import HealthController
from app.dtos.health import HealthResponse
from app.services.health import HealthService
from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])

health_controller = HealthController(health_service=HealthService())


@router.get("", response_model=HealthResponse, status_code=200)
async def health_check():
    """
    Health check endpoint.
    """
    return health_controller.get_health()
