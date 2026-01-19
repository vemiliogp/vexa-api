"""Lifespan management for application."""

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI


async def generate_insights():
    """Generate insights periodically."""
    while True:
        await asyncio.sleep(3600 * 1)
        print("Viva la arepa!")


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
