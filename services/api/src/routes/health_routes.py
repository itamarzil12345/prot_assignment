"""Health check routes."""

from fastapi import APIRouter
from pydantic import BaseModel

from shared.constants import Routes


router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    service: str


@router.get(Routes.HEALTH, response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint.

    Returns:
        HealthResponse with service status
    """
    return HealthResponse(status="healthy", service="protego-health-api")

