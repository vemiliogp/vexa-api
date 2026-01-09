"""Insight controller module."""

from dataclasses import dataclass

from app.dtos.insight import (
    CreateInsightsRequest,
    CreateInsightsResponse,
    GetInsightsResponse,
)
from app.services.insight import InsightService


@dataclass
class InsightController:
    """Controller to handle insight requests."""

    insight_service: InsightService

    async def create_insights(
        self, payload: CreateInsightsRequest, user_id: str
    ) -> CreateInsightsResponse:
        """
        Create new insights.
        """
        try:
            return await self.insight_service.create_insights(
                payload=payload, user_id=user_id
            )
        except Exception as e:
            raise e

    async def get_insights(self, user_id: str) -> GetInsightsResponse:
        """
        Retrieve all insights for a user.
        """
        try:
            return await self.insight_service.get_insights(user_id=user_id)
        except Exception as e:
            raise e
