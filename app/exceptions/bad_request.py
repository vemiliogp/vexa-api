"""Module defining a custom exception for bad requests."""

from fastapi.exceptions import HTTPException


class BadRequestException(HTTPException):
    """Exception raised for bad requests with status code 400."""

    def __init__(self, message="Bad Request"):
        super().__init__(status_code=400, detail=message)
