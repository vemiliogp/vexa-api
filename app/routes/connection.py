"""Connection routes module."""

from fastapi import APIRouter, Depends

from app.controllers.connection import ConnectionController
from app.dtos.connection import CreateConnectionRequest, CreateConnectionResponse
from app.middlewares.require_active_session import require_active_session
from app.services.connection import ConnectionService

router = APIRouter(prefix="/connection", tags=["Connection"])
connection_controller = ConnectionController(ConnectionService())


@router.post("/", response_model=CreateConnectionResponse, status_code=201)
async def create_connection(
    payload: CreateConnectionRequest, user=Depends(require_active_session)
):
    """
    Create a new connection endpoint.
    """
    connection = await connection_controller.create_connection(payload, user_id=user.id)
    return connection
