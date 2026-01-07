"""Exception handlers for FastAPI application."""

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


async def http_exception_handler(_request: Request, exc: HTTPException):
    """Handle HTTP exceptions with error_message format."""

    return JSONResponse(
        status_code=exc.status_code,
        content={"error_message": exc.detail},
    )
