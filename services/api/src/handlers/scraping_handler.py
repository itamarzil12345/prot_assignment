"""Handlers for scraping result operations."""

from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.handlers.base_handler import BaseHandler
from services.api.src.models.scraping_schema import (
    ScrapingResultResponse,
    ScrapingResultListResponse,
    ScrapingResultUpdateRequest,
    ScrapingResultQueryParams,
)
from services.api.src.repository.scraping_repository import ScrapingRepository
from services.api.src.errors.api_errors import APINotFoundError
from shared.constants import ErrorMessages
from shared.types.enums import SourceType


class ScrapingHandler(BaseHandler):
    """Handler for scraping result operations."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize scraping handler.

        Args:
            session: Database session
        """
        super().__init__(session)
        self._repository = ScrapingRepository(session)

    async def get_by_id(self, result_id: UUID) -> ScrapingResultResponse:
        """Get scraping result by ID.

        Args:
            result_id: UUID of the result

        Returns:
            ScrapingResultResponse

        Raises:
            APINotFoundError: If result not found
        """
        result = await self._repository.get_by_id(result_id)

        if not result:
            raise APINotFoundError(
                message=ErrorMessages.NOT_FOUND,
                error_code="SCRAPING_RESULT_NOT_FOUND",
                details={"result_id": str(result_id)},
            )

        return ScrapingResultResponse(
            id=result.id,
            source_type=result.source_type,
            external_id=result.external_id,
            title=result.title,
            data=result.data,
            link=result.link,
            scraped_at=result.scraped_at,
        )

    async def list_all(
        self, query_params: ScrapingResultQueryParams
    ) -> ScrapingResultListResponse:
        """List scraping results with pagination.

        Args:
            query_params: Query parameters for filtering and pagination

        Returns:
            ScrapingResultListResponse
        """
        results = await self._repository.list_all(
            limit=query_params.limit,
            offset=query_params.offset,
            source_type=query_params.source_type,
        )

        # Convert to response models
        items = [
            ScrapingResultResponse(
                id=result.id,
                source_type=result.source_type,
                external_id=result.external_id,
                title=result.title,
                data=result.data,
                link=result.link,
                scraped_at=result.scraped_at,
            )
            for result in results
        ]

        # TODO: Get total count for proper pagination
        # For now, use length of items as total
        total = len(items)

        return ScrapingResultListResponse(
            items=items,
            total=total,
            limit=query_params.limit,
            offset=query_params.offset,
        )

    async def update(
        self, result_id: UUID, updates: ScrapingResultUpdateRequest
    ) -> ScrapingResultResponse:
        """Update a scraping result.

        Args:
            result_id: UUID of the result to update
            updates: Update request data

        Returns:
            Updated ScrapingResultResponse

        Raises:
            APINotFoundError: If result not found
        """
        # Build update dict (only include non-None values)
        update_dict = {}
        if updates.title is not None:
            update_dict["title"] = updates.title
        if updates.data is not None:
            update_dict["data"] = updates.data

        if not update_dict:
            # No updates provided, return existing
            return await self.get_by_id(result_id)

        result = await self._repository.update(result_id, update_dict)

        return ScrapingResultResponse(
            id=result.id,
            source_type=result.source_type,
            external_id=result.external_id,
            title=result.title,
            data=result.data,
            link=result.link,
            scraped_at=result.scraped_at,
        )

    async def delete(self, result_id: UUID) -> None:
        """Delete a scraping result.

        Args:
            result_id: UUID of the result to delete

        Raises:
            APINotFoundError: If result not found
        """
        await self._repository.delete(result_id)

