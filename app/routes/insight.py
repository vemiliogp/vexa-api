"""Insight routes module."""

from fastapi import APIRouter, Depends

from app.controllers.insight import InsightController
from app.dtos.insight import (
    CreateInsightsRequest,
    CreateInsightsResponse,
    GetInsightsResponse,
)
from app.middlewares.require_active_session import require_active_session
from app.services.insight import InsightService

router = APIRouter(prefix="/insight", tags=["Insight"])

insight_service = InsightService()
insight_controller = InsightController(insight_service)


@router.post("/", response_model=CreateInsightsResponse, status_code=201)
async def create_insights(
    payload: CreateInsightsRequest, user=Depends(require_active_session)
):
    """
    Create new insights endpoint.
    """
    return await insight_controller.create_insights(payload, user_id=user.id)


@router.get("/", response_model=GetInsightsResponse, status_code=200)
async def get_insights(user=Depends(require_active_session)):
    """
    Retrieve all insights for a user endpoint.
    """
    return await insight_controller.get_insights(user_id=user.id)
