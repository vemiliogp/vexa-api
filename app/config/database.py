"""Database configuration registration."""

from os import getenv

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise


def setup_database(app: FastAPI) -> None:
    """Configure and register tortoise with application."""

    register_tortoise(
        app,
        db_url=getenv("DB_URL"),
        modules={"models": ["app.models"]},
        generate_schemas=True,
    )
