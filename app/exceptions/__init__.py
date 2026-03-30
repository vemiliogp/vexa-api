"""Exception handlers registration."""

from app.exceptions.http_exception_handler import http_exception_handler
from app.exceptions.unhandled_error_handler import unhandled_error_handler
from app.exceptions.validation_error_handler import validation_error_handler
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError


def register_exception_handlers(app: FastAPI) -> None:
    """Register all exception handlers on the FastAPI app."""

    # app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(Exception, unhandled_error_handler)
