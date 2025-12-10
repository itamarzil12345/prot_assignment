"""Handlers for analysis result operations."""

from uuid import UUID
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.handlers.base_handler import BaseHandler
from shared.types.enums import AnalysisType
from services.api.src.models.analysis_schema import (
    AnalysisResultResponse,
    AnalysisResultListResponse,
    AnalysisResultUpdateRequest,
    AnalysisResultQueryParams,
    MostFrequentTermsResponse,
    MostFrequentTermResponse,
)
from services.api.src.repository.analysis_repository import AnalysisRepository
from services.api.src.errors.api_errors import APINotFoundError
from shared.constants import ErrorMessages


class AnalysisHandler(BaseHandler):
    """Handler for analysis result operations."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize analysis handler.

        Args:
            session: Database session
        """
        super().__init__(session)
        self._repository = AnalysisRepository(session)

    async def get_by_id(self, result_id: UUID) -> AnalysisResultResponse:
        """Get analysis result by ID.

        Args:
            result_id: UUID of the result

        Returns:
            AnalysisResultResponse

        Raises:
            APINotFoundError: If result not found
        """
        result = await self._repository.get_by_id(result_id)

        if not result:
            raise APINotFoundError(
                message=ErrorMessages.NOT_FOUND,
                error_code="ANALYSIS_RESULT_NOT_FOUND",
                details={"result_id": str(result_id)},
            )

        return AnalysisResultResponse(
            id=result.id,
            scraping_result_id=result.scraping_result_id,
            analysis_type=result.analysis_type,
            keyword=result.keyword,
            frequency=result.frequency,
            metadata=result.metadata,
            created_at=result.created_at,
        )

    async def list_all(
        self, query_params: AnalysisResultQueryParams
    ) -> AnalysisResultListResponse:
        """List analysis results with pagination.

        Args:
            query_params: Query parameters for filtering and pagination

        Returns:
            AnalysisResultListResponse
        """
        results = await self._repository.list_all(
            limit=query_params.limit,
            offset=query_params.offset,
            analysis_type=query_params.analysis_type,
            scraping_result_id=query_params.scraping_result_id,
            keyword=query_params.keyword,
        )

        # Convert to response models
        items = [
            AnalysisResultResponse(
                id=result.id,
                scraping_result_id=result.scraping_result_id,
                analysis_type=result.analysis_type,
                keyword=result.keyword,
                frequency=result.frequency,
                metadata=result.metadata,
                created_at=result.created_at,
            )
            for result in results
        ]

        # Get total count for proper pagination
        total = await self._repository.count_all(
            analysis_type=query_params.analysis_type,
            scraping_result_id=query_params.scraping_result_id,
            keyword=query_params.keyword,
        )

        return AnalysisResultListResponse(
            items=items,
            total=total,
            limit=query_params.limit,
            offset=query_params.offset,
        )

    async def update(
        self, result_id: UUID, updates: AnalysisResultUpdateRequest
    ) -> AnalysisResultResponse:
        """Update an analysis result.

        Args:
            result_id: UUID of the result to update
            updates: Update request data

        Returns:
            Updated AnalysisResultResponse

        Raises:
            APINotFoundError: If result not found
        """
        # Build update dict
        update_dict = {}
        if updates.frequency is not None:
            update_dict["frequency"] = updates.frequency
        if updates.metadata is not None:
            update_dict["metadata"] = updates.metadata

        if not update_dict:
            # No updates provided, return existing
            return await self.get_by_id(result_id)

        result = await self._repository.update(result_id, update_dict)

        return AnalysisResultResponse(
            id=result.id,
            scraping_result_id=result.scraping_result_id,
            analysis_type=result.analysis_type,
            keyword=result.keyword,
            frequency=result.frequency,
            metadata=result.metadata,
            created_at=result.created_at,
        )

    async def delete(self, result_id: UUID) -> None:
        """Delete an analysis result.

        Args:
            result_id: UUID of the result to delete

        Raises:
            APINotFoundError: If result not found
        """
        await self._repository.delete(result_id)

    async def get_most_frequent_terms(
        self,
        limit: int,
        analysis_type: Optional[AnalysisType] = None,
    ) -> MostFrequentTermsResponse:
        """Get most frequent terms across all analysis results.

        Args:
            limit: Maximum number of terms to return
            analysis_type: Optional filter by analysis type

        Returns:
            MostFrequentTermsResponse with list of most frequent terms
        """
        results = await self._repository.get_most_frequent_terms(
            limit=limit,
            analysis_type=analysis_type,
        )

        items = [
            MostFrequentTermResponse(
                keyword=result["keyword"],
                total_frequency=result["total_frequency"],
                document_count=result["document_count"],
            )
            for result in results
        ]

        return MostFrequentTermsResponse(items=items, limit=limit)

