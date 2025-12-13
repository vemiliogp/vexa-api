"""Connection routes module."""

from fastapi import APIRouter, Depends

from app.controllers.connection import ConnectionController
from app.dtos.connection import (
    CheckConnectionResponse,
    CreateConnectionRequest,
    CreateConnectionResponse,
    GetConnectionsResponse,
)
from app.middlewares.require_active_session import require_active_session
from app.services.connection import ConnectionService
from app.services.database import DatabaseService

router = APIRouter(prefix="/connection", tags=["Connection"])

connection_service = ConnectionService(DatabaseService())
connection_controller = ConnectionController(connection_service)


@router.post("/", response_model=CreateConnectionResponse, status_code=201)
async def create_connection(
    payload: CreateConnectionRequest, user=Depends(require_active_session)
):
    """
    Create a new connection endpoint.
    """
    connection = await connection_controller.create_connection(payload, user_id=user.id)
    return connection


@router.get("/", response_model=GetConnectionsResponse, status_code=200)
async def get_connections(user=Depends(require_active_session)):
    """
    Retrieve all connections for a user endpoint.
    """
    connections = await connection_controller.get_connections(user_id=user.id)
    return connections


@router.get(
    "/{connection_id}/check", response_model=CheckConnectionResponse, status_code=200
)
async def check_connection(connection_id: str, user=Depends(require_active_session)):
    """
    Test if a connection is working properly endpoint.
    """
    r = await connection_controller.check_connection(connection_id, user_id=user.id)
    return r
