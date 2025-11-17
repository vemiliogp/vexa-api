"""Connection service module."""

from dataclasses import dataclass

from app.dtos.connection import CreateConnectionRequest, CreateConnectionResponse
from app.models.connection import Connection


@dataclass
class ConnectionService:
    """Service to handle connections."""

    async def create_connection(
        self, payload: CreateConnectionRequest
    ) -> CreateConnectionResponse:
        """
        Register a new connection by user.
        """
        try:
            connection = await Connection.create(
                name=payload.name,
                description=payload.description,
                engine=payload.engine,
                url=payload.url,
            )

            return CreateConnectionResponse(
                id=connection.id,
                name=connection.name,
                description=connection.description,
                engine=connection.engine,
                url=connection.url,
            )
        except Exception as e:
            raise e
