"""Middleware registration."""

from os import getenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware


def setup_middlewares(app: FastAPI) -> None:
    """Configure and add all middlewares to the application."""

    app.add_middleware(
        SessionMiddleware,
        secret_key=getenv("SESSION_SECRET"),
        session_cookie="vexa_session",
        max_age=60 * 60 * 24,
        same_site="lax",
        https_only=False,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            origin.strip() for origin in getenv("CORS_ALLOWED_ORIGINS").split(",")
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
