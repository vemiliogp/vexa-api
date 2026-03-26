"""Lifespan management for application."""

import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

logger = logging.getLogger(__name__)


async def generate_insights():
    """Generate insights periodically for all connections."""
    from app.agent.agent import Agent
    from app.agent.prompts.agent_insight_prompt import get_agent_insight_prompt
    from app.models.connection import Connection
    from app.models.insight import Insight
    from app.services.database import DatabaseService
    from app.utils.encrypt import Encrypt

    while True:
        await asyncio.sleep(3600 * 24)
        try:
            connections = await Connection.all().select_related("user")
            logger.info(f"Generating insights for {len(connections)} connections")

            for connection in connections:
                try:
                    connection_url = Encrypt.decrypt(connection.encrypted_url)
                    tables = DatabaseService.get_tables(connection_url)

                    if not tables:
                        logger.info(
                            f"Skipping insight for connection {connection.id}: no tables found"
                        )
                        continue

                    existing_insights_list = await Insight.filter(
                        user_id=connection.user_id,
                        connection_id=connection.id,
                    ).all()
                    existing_insights_text = "\n".join(
                        [
                            f"- Título: {i.title}. Descripción: {i.description[:200]}..."
                            for i in existing_insights_list
                        ]
                    )

                    system_prompt = get_agent_insight_prompt(
                        tables=str(tables),
                        context=None,
                        num_insights=1,
                        db_engine=connection.engine,
                        existing_insights=existing_insights_text,
                    )

                    agent = Agent(
                        model="deepseek/r1",
                        connection_url=connection_url,
                        system_prompt=system_prompt,
                        user_id=connection.user_id,
                        connection_id=connection.id,
                    )

                    loop = asyncio.get_event_loop()
                    await loop.run_in_executor(None, agent.run)

                    logger.info(
                        f"Insight generated for connection {connection.id} "
                        f"(user {connection.user_id})"
                    )
                except Exception as e:
                    logger.error(
                        f"Error generating insight for connection {connection.id}: {e}"
                    )
        except Exception as e:
            logger.error(f"Error in periodic insight generation: {e}")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Application lifespan manager for background tasks."""
    tasks = [
        asyncio.create_task(generate_insights()),
    ]
    yield
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)
