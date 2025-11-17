"""Connection controller module."""

from dataclasses import dataclass

from app.dtos.connection import CreateConnectionRequest, CreateConnectionResponse
from app.services.connection import ConnectionService


@dataclass
class ConnectionController:
    """Controller to handle connection requests."""

    connection_service: ConnectionService

    def create_connection(
        self, payload: CreateConnectionRequest
    ) -> CreateConnectionResponse:
        """
        Create a new connection by delegating to the ConnectionService.
        """
        return self.connection_service.create_connection(payload)
