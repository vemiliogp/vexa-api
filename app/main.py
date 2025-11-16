"""Main entry point for the application."""

from os import getenv

from dotenv import load_dotenv
from fastapi import FastAPI
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

register_routes(app)

register_tortoise(
    app,
    db_url=getenv("DB_URL"),
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
