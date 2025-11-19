"""
Router registration.
"""

from fastapi import FastAPI

from app.routes.auth import router as auth_router
from app.routes.connection import router as connection_router
from app.routes.health import router as health_router
from app.routes.conversation import router as conversation_router


def register_routes(app: FastAPI) -> None:
    """
    Register all application routes.
    """

    app.include_router(health_router)
    app.include_router(auth_router)
    app.include_router(connection_router)
    app.include_router(conversation_router)
