"""Main entry point for the application."""

from dotenv import load_dotenv

load_dotenv()

import mlflow
from fastapi import FastAPI

from app.config.database import setup_database
from app.config.lifespan import lifespan
from app.config.middlewares import setup_middlewares
from app.exceptions import register_exception_handlers
from app.routes import register_routes

mlflow.set_experiment("Vexa")
mlflow.litellm.autolog()

app = FastAPI(lifespan=lifespan)

setup_middlewares(app)
register_routes(app)
setup_database(app)
register_exception_handlers(app)
