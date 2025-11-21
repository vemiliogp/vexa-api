"""Conversation routes module."""

from fastapi import APIRouter, Depends, File, UploadFile

from app.controllers.conversation import ConversationController
from app.dtos.conversation import CreateConversationRequest, CreateConversationResponse
from app.middlewares.require_active_session import require_active_session
from app.services.conversation import ConversationService
from app.services.message import MessageService

router = APIRouter(prefix="/conversation", tags=["Conversation"])
conversation_service = ConversationService(MessageService())
conversation_controller = ConversationController(conversation_service)


@router.post("/", response_model=CreateConversationResponse, status_code=201)
async def create_conversation(
    payload: CreateConversationRequest, user=Depends(require_active_session)
):
    """
    Create a new conversation endpoint.
    """
    conversation = await conversation_controller.create_conversation(
        payload, user_id=user.id
    )
    return conversation


@router.get("/", status_code=200)
async def get_conversations(user=Depends(require_active_session)):
    """
    Retrieve all conversations for a user endpoint.
    """
    conversations = await conversation_controller.get_conversations(user_id=user.id)
    return conversations


@router.post("/{conversation_id}/message/text", status_code=200)
async def send_message(
    conversation_id: str, payload: dict, user=Depends(require_active_session)
):
    """
    Send a message in a conversation endpoint.
    """
    response = await conversation_controller.send_message(
        payload, user_id=user.id, conversation_id=conversation_id
    )
    return response


@router.post("/{conversation_id}/message/audio", status_code=200)
async def send_audio_message(
    conversation_id: str,
    file: UploadFile = File(...),
    user=Depends(require_active_session),
):
    """
    Send an audio message in a conversation endpoint.
    """
    response = await conversation_controller.send_audio_message(
        file=file, user_id=user.id, conversation_id=conversation_id
    )
    return response


@router.get("/{conversation_id}/messages", status_code=200)
async def get_messages(conversation_id: str, user=Depends(require_active_session)):
    """
    Retrieve messages from a conversation endpoint.
    """
    messages = await conversation_controller.get_messages(
        conversation_id=conversation_id
    )
    return messages
