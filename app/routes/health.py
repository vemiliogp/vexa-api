"""Health routes module."""

from fastapi import APIRouter

from app.controllers.health import HealthController
from app.services.health import HealthService

router = APIRouter()

health_controller = HealthController(health_service=HealthService())


@router.get("/v1/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    """
    return health_controller.get_health()
