"""Connection routes module."""

from fastapi import APIRouter

from app.controllers.connection import ConnectionController
from app.dtos.connection import CreateConnectionRequest, CreateConnectionResponse
from app.services.connection import ConnectionService

router = APIRouter(prefix="/connection", tags=["Connection"])
connection_controller = ConnectionController(ConnectionService())


@router.post("/", response_model=CreateConnectionResponse, status_code=201)
async def create_connection(payload: CreateConnectionRequest):
    """
    Create a new connection endpoint.
    """
    connection = await connection_controller.create_connection(payload)
    return connection
