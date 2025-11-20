"""Module defining a custom exception for bad requests."""


class BadRequestException(Exception):
    """Exception raised for bad requests with status code 400."""

    def __init__(self, message="Bad Request", status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
