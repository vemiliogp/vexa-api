"""Conversation routes module."""

from fastapi import APIRouter, Depends

from app.controllers.conversation import ConversationController
from app.dtos.conversation import CreateConversationRequest, CreateConversationResponse
from app.middlewares.session import require_active_session
from app.services.conversation import ConversationService

router = APIRouter(prefix="/conversation", tags=["Conversation"])
conversation_controller = ConversationController(ConversationService())


@router.post("/", response_model=CreateConversationResponse, status_code=201)
async def create_conversation(
    payload: CreateConversationRequest, user=Depends(require_active_session)
):
    """
    Create a new conversation endpoint.
    """
    conversation = await conversation_controller.create_conversation(payload)
    return conversation
