"""Connection controller module."""

from dataclasses import dataclass

from app.dtos.connection import (
    CreateConnectionRequest,
    CreateConnectionResponse,
    GetConnectionsResponse,
)
from app.services.connection import ConnectionService


@dataclass
class ConnectionController:
    """Controller to handle connection requests."""

    connection_service: ConnectionService

    async def create_connection(
        self, payload: CreateConnectionRequest, user_id: str
    ) -> CreateConnectionResponse:
        """
        Create a new connection.
        """
        try:
            return await self.connection_service.create_connection(
                payload=payload, user_id=user_id
            )
        except Exception as e:
            raise e

    async def get_connections(self, user_id: str) -> GetConnectionsResponse:
        """
        Retrieve all connections for a user.
        """
        try:
            return await self.connection_service.get_connections(user_id=user_id)
        except Exception as e:
            raise e
