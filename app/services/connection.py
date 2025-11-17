"""Connection service module."""

from dataclasses import dataclass

from app.dtos.connection import CreateConnectionRequest, CreateConnectionResponse
from app.models.connection import Connection
from app.utils.encrypt import Encrypt


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
            encrypted_url = Encrypt.encrypt(payload.url)

            connection = await Connection.create(
                name=payload.name,
                description=payload.description,
                engine=payload.engine,
                encrypted_url=encrypted_url,
                user_id=1,
            )

            return CreateConnectionResponse(
                id=connection.id,
                name=connection.name,
                description=connection.description,
                engine=connection.engine,
                url=connection.encrypted_url,
            )
        except Exception as e:
            raise e
