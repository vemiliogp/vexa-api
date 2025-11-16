"""Main entry point for the application."""

from fastapi import FastAPI

from app.routes import register_routes

app = FastAPI()

register_routes(app)
