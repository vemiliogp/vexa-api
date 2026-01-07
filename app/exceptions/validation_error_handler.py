"""Exception handlers for FastAPI application."""

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def validation_error_handler(_request: Request, exc: RequestValidationError):
    """Handle validation errors with clearer messages."""
    errors = []
    for error in exc.errors():
        field = ".".join(str(x) for x in error["loc"][1:])
        msg = error["msg"]
        errors.append({"field": field, "message": msg})

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error_message": "Validation error", "errors": errors},
    )
