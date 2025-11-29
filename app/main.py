"""Main entry point for the application."""

from os import getenv

from dotenv import load_dotenv
from fastapi import FastAPI, Request, status
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
    add_exception_handlers=True,
)


@app.exception_handler(Exception)
async def unhandled_error_handler(request: Request, exc: Exception):
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
