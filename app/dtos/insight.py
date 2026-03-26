"""DTOs for insight endpoints."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class DeliveryMethod(str, Enum):
    """Delivery method for insights."""

    EMAIL = "email"
    IN_APP = "in_app"


class InsightData(BaseModel):
    """Shared insight data dto."""

    id: int
    title: str | None = None
    description: str | None = None
    created_at: datetime | None = None
    connection_id: int | None = None
    connection_name: str | None = None


class CreateInsightsRequest(BaseModel):
    """Payload expected by the create insight endpoint."""

    context: str | None = Field(default=None)
    count: int = Field(default=1, ge=1, le=5)
    connection_id: int | None = Field(default=None)
    delivery_method: DeliveryMethod = Field(default=DeliveryMethod.IN_APP)


class CreateInsightsResponse(BaseModel):
    """Response returned by the create insight endpoint."""

    message: str = "Insights created successfully"


class GetInsightsResponse(BaseModel):
    """Response returned by the get insights endpoint."""

    data: list[InsightData] = Field(default_factory=list)
    message: str = "Insights retrieved successfully"
