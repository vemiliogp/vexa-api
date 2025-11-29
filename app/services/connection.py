"""Connection service module."""

from dataclasses import dataclass

from app.dtos.connection import (
    ConnectionProfile,
    CreateConnectionRequest,
    CreateConnectionResponse,
)
from app.models.connection import Connection
from app.utils.encrypt import Encrypt


@dataclass
class ConnectionService:
    """Service to handle connections."""

    async def create_connection(
        self, payload: CreateConnectionRequest, user_id: str
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
                user_id=user_id,
            )

            profile = ConnectionProfile(
                id=connection.id,
                name=connection.name,
                description=connection.description,
                engine=connection.engine,
            )

            return CreateConnectionResponse(
                data=profile,
                message="Connection created successfully",
            )
        except Exception as e:
            raise e
