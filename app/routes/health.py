"""Health routes module."""

from fastapi import APIRouter

from app.controllers.health import HealthController
from app.services.health import HealthService

router = APIRouter(prefix="/health", tags=["Health"])

health_controller = HealthController(health_service=HealthService())


@router.get("", status_code=200)
async def health_check():
    """
    Health check endpoint.
    """
    return health_controller.get_health()
