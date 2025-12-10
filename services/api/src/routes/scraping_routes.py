"""Routes for scraping result operations."""

from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.database.base import get_db_session
from services.api.src.handlers.scraping_handler import ScrapingHandler
from services.api.src.models.scraping_schema import (
    ScrapingResultResponse,
    ScrapingResultListResponse,
    ScrapingResultUpdateRequest,
    ScrapingResultQueryParams,
)
from shared.constants import Routes
from shared.types.enums import SourceType


router = APIRouter(prefix=Routes.SCRAPING, tags=["scraping"])


@router.get(
    "/{result_id}",
    response_model=ScrapingResultResponse,
    summary="Get scraping result by ID",
    description="Retrieve a single scraping result by its UUID",
)
async def get_scraping_result(
    result_id: UUID,
    session: AsyncSession = Depends(get_db_session),
) -> ScrapingResultResponse:
    """Get scraping result by ID."""
    handler = ScrapingHandler(session)
    return await handler.get_by_id(result_id)


@router.get(
    "",
    response_model=ScrapingResultListResponse,
    summary="List scraping results",
    description="List scraping results with pagination and optional filtering",
)
async def list_scraping_results(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    source_type: SourceType | None = Query(default=None),
    session: AsyncSession = Depends(get_db_session),
) -> ScrapingResultListResponse:
    """List scraping results with pagination."""
    handler = ScrapingHandler(session)
    query_params = ScrapingResultQueryParams(
        limit=limit, offset=offset, source_type=source_type
    )
    return await handler.list_all(query_params)


@router.put(
    "/{result_id}",
    response_model=ScrapingResultResponse,
    summary="Update scraping result",
    description="Update fields of an existing scraping result",
)
async def update_scraping_result(
    result_id: UUID,
    updates: ScrapingResultUpdateRequest,
    session: AsyncSession = Depends(get_db_session),
) -> ScrapingResultResponse:
    """Update scraping result."""
    handler = ScrapingHandler(session)
    return await handler.update(result_id, updates)


@router.delete(
    "/{result_id}",
    status_code=204,
    summary="Delete scraping result",
    description="Delete a scraping result by its UUID",
)
async def delete_scraping_result(
    result_id: UUID,
    session: AsyncSession = Depends(get_db_session),
) -> None:
    """Delete scraping result."""
    handler = ScrapingHandler(session)
    await handler.delete(result_id)

