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
    MostFrequentTermsResponse,
)
from shared.constants import Routes
from shared.types.enums import AnalysisType


router = APIRouter(prefix=Routes.ANALYSIS, tags=["analysis"])


@router.get(
    "/most-frequent",
    response_model=MostFrequentTermsResponse,
    summary="Get most frequent terms",
    description="Get the most frequently occurring keywords across all analysis results. Returns aggregated statistics including total frequency across all documents and the number of documents containing each keyword. Results are ordered by total frequency (descending).",
)
async def get_most_frequent_terms(
    limit: int = Query(default=10, ge=1, le=100, description="Number of top terms to return (1-100). Returns the N most frequent keywords."),
    analysis_type: AnalysisType | None = Query(default=None, description="Optional filter by analysis type. If provided, only counts terms from the specified analysis type."),
    session: AsyncSession = Depends(get_db_session),
) -> MostFrequentTermsResponse:
    """Get most frequent terms across all analysis results with aggregated statistics."""
    handler = AnalysisHandler(session)
    return await handler.get_most_frequent_terms(limit=limit, analysis_type=analysis_type)


@router.get(
    "",
    response_model=AnalysisResultListResponse,
    summary="List analysis results",
    description="List analysis results with pagination and optional filtering. Supports filtering by analysis type, scraping result ID, and keyword.",
)
async def list_analysis_results(
    limit: int = Query(default=50, ge=1, le=100, description="Maximum number of results per page (1-100)"),
    offset: int = Query(default=0, ge=0, description="Number of results to skip for pagination"),
    analysis_type: AnalysisType | None = Query(default=None, description="Filter by analysis type (KEYWORD_FREQUENCY, CONDITION_GROUPING, CATEGORY_GROUPING)"),
    scraping_result_id: UUID | None = Query(default=None, description="Filter by scraping result UUID"),
    keyword: str | None = Query(default=None, description="Filter by keyword (case-insensitive exact match). Returns all entries where the keyword exactly matches this value."),
    session: AsyncSession = Depends(get_db_session),
) -> AnalysisResultListResponse:
    """List analysis results with pagination and filtering options."""
    handler = AnalysisHandler(session)
    query_params = AnalysisResultQueryParams(
        limit=limit,
        offset=offset,
        analysis_type=analysis_type,
        scraping_result_id=scraping_result_id,
        keyword=keyword,
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

