"""Auth service module."""

from dataclasses import dataclass

from fastapi import HTTPException, status

from app.dtos.insight import (
    CreateInsightsRequest,
    CreateInsightsResponse,
    GetInsightsResponse,
    InsightData,
)
from app.models.insight import Insight


@dataclass
class InsightService:
    """Service to handle insights."""

    async def create_insights(
        self, payload: CreateInsightsRequest, user_id: str
    ) -> CreateInsightsResponse:
        """
        Create new insights.
        """
        pass

    async def get_insights(self, user_id: str) -> GetInsightsResponse:
        """
        Get all insights for a user.
        """
        try:
            insights = await Insight.filter(user_id=user_id).all()
            data = [
                InsightData(
                    id=insight.id,
                    title=insight.title,
                    description=insight.description,
                )
                for insight in insights
            ]
            return GetInsightsResponse(data=data)
        except Exception as e:
            raise e
