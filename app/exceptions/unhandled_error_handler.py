"""Exception handlers for FastAPI application."""

from fastapi import Request, status
from fastapi.responses import JSONResponse


async def unhandled_error_handler(_request: Request, exc: Exception):
    """Handle unexpected errors."""
    return JSONResponse(
        status_code=(
            exc.status_code
            if hasattr(exc, "status_code")
            else status.HTTP_500_INTERNAL_SERVER_ERROR
        ),
        content={
            "detail": (
                str(exc.message) if hasattr(exc, "message") else "An unexpected error occurred"
            )
        },
    )
