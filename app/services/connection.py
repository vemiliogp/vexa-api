"""Connection service module."""

from dataclasses import dataclass

from app.dtos.connection import (
    CheckConnectionResponse,
    ConnectionData,
    CreateConnectionRequest,
    CreateConnectionResponse,
    GetConnectionsResponse,
)
from app.exceptions.bad_request import BadRequestException
from app.models.connection import Connection
from app.services.database import DatabaseService
from app.utils.encrypt import Encrypt


@dataclass
class ConnectionService:
    """Service to handle connections."""

    database_service: DatabaseService

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

            data = ConnectionData(
                id=connection.id,
                name=connection.name,
                description=connection.description,
                engine=connection.engine,
            )

            return CreateConnectionResponse(
                data=data,
                message="Connection created successfully",
            )
        except Exception as e:
            raise e

    async def get_connections(self, user_id: str) -> GetConnectionsResponse:
        """
        Retrieve all connections for a user.
        """
        try:
            connections = await Connection.filter(user_id=user_id).all()
            data = [
                ConnectionData(
                    id=connection.id,
                    name=connection.name,
                    description=connection.description,
                    engine=connection.engine,
                )
                for connection in connections
            ]
            return GetConnectionsResponse(data=data)
        except Exception as e:
            raise e

    async def check_connection(
        self, connection_id: str, user_id: str
    ) -> CheckConnectionResponse:
        """
        Check connection
        """
        try:
            connection = await Connection.get_or_none(id=connection_id, user_id=user_id)
            if not connection:
                raise BadRequestException("Connection not found")

            connection_url = Encrypt.decrypt(connection.encrypted_url)

            status = self.database_service.check_connection(connection_url)

            return CheckConnectionResponse(success=status)
        except Exception as e:
            raise e
