"""Insight service module."""

import asyncio
import logging
from dataclasses import dataclass

from fastapi import HTTPException, status

logger = logging.getLogger(__name__)

from app.agent.agent import Agent
from app.agent.prompts.agent_insight_prompt import get_agent_insight_prompt
from app.dtos.insight import (
    CreateInsightsRequest,
    CreateInsightsResponse,
    DeliveryMethod,
    GetInsightsResponse,
    InsightData,
)
from app.models.connection import Connection
from app.models.insight import Insight
from app.models.user import User
from app.services.database import DatabaseService
from app.services.email import EmailService, SendMailOptions
from app.utils.encrypt import Encrypt


@dataclass
class InsightService:
    """Service to handle insights."""

    async def _send_insights_email(
        self, user_id: str, connection_id: int, count: int
    ) -> None:
        try:
            user = await User.get(id=int(user_id))
            insights = (
                await Insight.filter(user_id=user_id, connection_id=connection_id)
                .order_by("-created_at")
                .limit(count)
                .all()
            )
            items = "".join(
                f"<h3>{i.title}</h3><p>{i.description}</p><hr/>" for i in insights
            )
            html_body = f"<html><body><h2>Tus nuevos insights</h2>{items}</body></html>"
            options = SendMailOptions(
                to=user.email,
                subject="Tus nuevos insights están listos",
                html_body=html_body,
            )
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, lambda: EmailService().send_email(options))
        except Exception:
            logger.exception("Failed to send insights email for user %s", user_id)

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

            tables = DatabaseService.get_tables_with_columns(connection_url)

            existing_insights_list = await Insight.filter(
                user_id=user_id, connection_id=connection.id
            ).all()
            existing_insights_text = "\n".join(
                [
                    f"- Título: {i.title}. Descripción: {i.description[:200]}..."
                    for i in existing_insights_list
                ]
            )

            system_prompt = get_agent_insight_prompt(
                tables=str(tables),
                context=payload.context,
                num_insights=payload.count,
                db_engine=connection.engine,
                existing_insights=existing_insights_text,
            )

            agent = Agent(
                model="openai/gpt-oss",
                connection_url=connection_url,
                system_prompt=system_prompt,
                user_id=int(user_id),
                connection_id=connection.id,
            )

            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, agent.run)

            if payload.delivery_method == DeliveryMethod.EMAIL:
                asyncio.create_task(
                    self._send_insights_email(user_id, connection.id, payload.count)
                )

            return CreateInsightsResponse()
        except Exception as e:
            raise e

    async def get_insights(self, user_id: str) -> GetInsightsResponse:
        """
        Get all insights for a user.
        """
        try:
            insights = (
                await Insight.filter(user_id=user_id)
                .order_by("-created_at")
                .select_related("connection")
                .all()
            )
            data = [
                InsightData(
                    id=insight.id,
                    title=insight.title,
                    description=insight.description,
                    created_at=insight.created_at,
                    connection_id=insight.connection_id,
                    connection_name=(
                        insight.connection.name if insight.connection else None
                    ),
                )
                for insight in insights
            ]
            return GetInsightsResponse(data=data)
        except Exception as e:
            raise e
