"""Main entry point for the application."""

from os import getenv

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from tortoise.contrib.fastapi import register_tortoise

from app.routes import register_routes

load_dotenv()

app = FastAPI()


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
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_routes(app)

register_tortoise(
    app,
    db_url=getenv("DB_URL"),
    modules={"models": ["app.models"]},
    generate_schemas=True,
)


@app.exception_handler(HTTPException)
async def http_exception_handler(_request: Request, exc: HTTPException):
    """Handle HTTP exceptions with error_message format."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error_message": exc.detail},
    )


@app.exception_handler(RequestValidationError)
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


@app.exception_handler(Exception)
async def unhandled_error_handler(_request: Request, exc: Exception):
    """Handle validation with errors unexpected."""
    return JSONResponse(
        status_code=(
            exc.status_code
            if hasattr(exc, "status_code")
            else status.HTTP_500_INTERNAL_SERVER_ERROR
        ),
        content={
            "error_message": (
                str(exc.message) if hasattr(exc, "message") else "Internal Server Error"
            )
        },
    )
