"""Insight service module."""

from dataclasses import dataclass

from fastapi import HTTPException, status

from app.agent.agent_insight import AgentInsight
from app.dtos.insight import (
    CreateInsightsRequest,
    CreateInsightsResponse,
    GetInsightsResponse,
    InsightData,
)
from app.models.connection import Connection
from app.models.insight import Insight
from app.services.database import DatabaseService
from app.utils.encrypt import Encrypt


@dataclass
class InsightService:
    """Service to handle insights."""

    async def create_insights(
        self, payload: CreateInsightsRequest, user_id: str
    ) -> CreateInsightsResponse:
        """
        Create new insights.
        """
        try:
            connection = await Connection.get_or_none(
                id=payload.connection_id, user_id=user_id
            )
            if not connection:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Connection not found",
                )

            connection_url = Encrypt.decrypt(connection.encrypted_url)

            tables = DatabaseService.get_tables(connection_url)

            agent = AgentInsight(
                model="deepseek/r1",
                connection_url=connection_url,
                context=payload.context,
                tables=str(tables),
            )

            agent.run(num_insights=payload.count)

            return CreateInsightsResponse()
        except Exception as e:
            raise e

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
