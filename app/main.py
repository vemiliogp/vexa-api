"""Main entry point for the application."""

from os import getenv

from dotenv import load_dotenv
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.routes import register_routes

app = FastAPI()

load_dotenv()

register_routes(app)

register_tortoise(
    app,
    db_url=getenv("DATABASE_URL"),
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
