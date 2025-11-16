"""
Router registration.
"""

from fastapi import FastAPI

from app.routes.health import router as health_router


def register_routes(app: FastAPI) -> None:
    """
    Register all application routes.
    """

    app.include_router(health_router)
