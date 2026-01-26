"""Insight service module."""

from dataclasses import dataclass

from fastapi import HTTPException, status

from app.agent.agent import Agent
from app.agent.prompts.agent_insight_prompt import get_agent_insight_prompt
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

            system_prompt = get_agent_insight_prompt(
                tables=str(tables),
                context=payload.context,
                num_insights=payload.count,
            )

            agent = Agent(
                model="deepseek/r1",
                connection_url=connection_url,
                system_prompt=system_prompt,
                user_id=int(user_id),
                connection_id=connection.id,
            )

            agent.run()

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
