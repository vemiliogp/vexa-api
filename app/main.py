"""Main entry point for the application."""

from dotenv import load_dotenv
from fastapi import FastAPI

import mlflow

mlflow.litellm.autolog()

from app.config.database import setup_database
from app.config.lifespan import lifespan
from app.config.middlewares import setup_middlewares
from app.exceptions import register_exception_handlers
from app.routes import register_routes

load_dotenv()

app = FastAPI(lifespan=lifespan)

setup_middlewares(app)
register_routes(app)
setup_database(app)
register_exception_handlers(app)
