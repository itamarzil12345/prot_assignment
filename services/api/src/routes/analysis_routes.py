"""Routes for analysis result operations."""

from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.database.base import get_db_session
from services.api.src.handlers.analysis_handler import AnalysisHandler
from services.api.src.models.analysis_schema import (
    AnalysisResultResponse,
    AnalysisResultListResponse,
    AnalysisResultUpdateRequest,
    AnalysisResultQueryParams,
)
from shared.constants import Routes
from shared.types.enums import AnalysisType


router = APIRouter(prefix=Routes.ANALYSIS, tags=["analysis"])


@router.get(
    "/{result_id}",
    response_model=AnalysisResultResponse,
    summary="Get analysis result by ID",
    description="Retrieve a single analysis result by its UUID",
)
async def get_analysis_result(
    result_id: UUID,
    session: AsyncSession = Depends(get_db_session),
) -> AnalysisResultResponse:
    """Get analysis result by ID."""
    handler = AnalysisHandler(session)
    return await handler.get_by_id(result_id)


@router.get(
    "",
    response_model=AnalysisResultListResponse,
    summary="List analysis results",
    description="List analysis results with pagination and optional filtering",
)
async def list_analysis_results(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    analysis_type: AnalysisType | None = Query(default=None),
    scraping_result_id: UUID | None = Query(default=None),
    session: AsyncSession = Depends(get_db_session),
) -> AnalysisResultListResponse:
    """List analysis results with pagination."""
    handler = AnalysisHandler(session)
    query_params = AnalysisResultQueryParams(
        limit=limit,
        offset=offset,
        analysis_type=analysis_type,
        scraping_result_id=scraping_result_id,
    )
    return await handler.list_all(query_params)


@router.put(
    "/{result_id}",
    response_model=AnalysisResultResponse,
    summary="Update analysis result",
    description="Update fields of an existing analysis result",
)
async def update_analysis_result(
    result_id: UUID,
    updates: AnalysisResultUpdateRequest,
    session: AsyncSession = Depends(get_db_session),
) -> AnalysisResultResponse:
    """Update analysis result."""
    handler = AnalysisHandler(session)
    return await handler.update(result_id, updates)


@router.delete(
    "/{result_id}",
    status_code=204,
    summary="Delete analysis result",
    description="Delete an analysis result by its UUID",
)
async def delete_analysis_result(
    result_id: UUID,
    session: AsyncSession = Depends(get_db_session),
) -> None:
    """Delete analysis result."""
    handler = AnalysisHandler(session)
    await handler.delete(result_id)

