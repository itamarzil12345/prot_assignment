"""Repository implementation for analysis results."""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, not_
from sqlalchemy.orm import selectinload

from services.api.src.database.models import (
    AnalysisResultModel,
    ScrapingResultModel,
)
from services.analysis.src.repository.analysis_repository_interface import (
    AnalysisRepositoryInterface,
    AnalysisResultDTO,
)
from shared.errors import DatabaseError
from shared.types.enums import AnalysisType


class AnalysisRepository(AnalysisRepositoryInterface):
    """SQLAlchemy implementation of analysis repository."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize repository with database session.

        Args:
            session: Async database session
        """
        self._session = session

    async def create(self, result: AnalysisResultDTO) -> UUID:
        """Create a new analysis result."""
        try:
            model = AnalysisResultModel(
                id=result.id,
                scraping_result_id=result.scraping_result_id,
                analysis_type=result.analysis_type,
                keyword=result.keyword,
                frequency=result.frequency,
                meta_data=result.metadata,
                created_at=result.created_at,
            )

            self._session.add(model)
            await self._session.flush()
            return model.id

        except Exception as e:
            raise DatabaseError(
                message="Failed to create analysis result",
                error_code="ANALYSIS_RESULT_CREATE_ERROR",
                details={"error": str(e)},
            ) from e

    async def create_batch(self, results: List[AnalysisResultDTO]) -> List[UUID]:
        """Create multiple analysis results in batch."""
        try:
            models = [
                AnalysisResultModel(
                    id=result.id,
                    scraping_result_id=result.scraping_result_id,
                    analysis_type=result.analysis_type,
                    keyword=result.keyword,
                    frequency=result.frequency,
                    meta_data=result.metadata,
                    created_at=result.created_at,
                )
                for result in results
            ]

            self._session.add_all(models)
            await self._session.flush()

            return [model.id for model in models]

        except Exception as e:
            raise DatabaseError(
                message="Failed to create analysis results in batch",
                error_code="ANALYSIS_RESULT_BATCH_CREATE_ERROR",
                details={"error": str(e), "count": len(results)},
            ) from e

    async def get_by_id(self, result_id: UUID) -> Optional[AnalysisResultDTO]:
        """Get analysis result by ID."""
        try:
            stmt = select(AnalysisResultModel).where(
                AnalysisResultModel.id == result_id
            )
            result = await self._session.execute(stmt)
            model = result.scalar_one_or_none()

            if not model:
                return None

            return AnalysisResultDTO(
                id=model.id,
                scraping_result_id=model.scraping_result_id,
                analysis_type=model.analysis_type,
                keyword=model.keyword,
                frequency=model.frequency,
                metadata=model.meta_data,
                created_at=model.created_at,
            )

        except Exception as e:
            raise DatabaseError(
                message="Failed to get analysis result by ID",
                error_code="ANALYSIS_RESULT_GET_ERROR",
                details={"error": str(e), "result_id": str(result_id)},
            ) from e

    async def get_by_scraping_result_id(
        self, scraping_result_id: UUID
    ) -> List[AnalysisResultDTO]:
        """Get all analysis results for a scraping result."""
        try:
            stmt = select(AnalysisResultModel).where(
                AnalysisResultModel.scraping_result_id == scraping_result_id
            )
            result = await self._session.execute(stmt)
            models = result.scalars().all()

            return [
                AnalysisResultDTO(
                    id=model.id,
                    scraping_result_id=model.scraping_result_id,
                    analysis_type=model.analysis_type,
                    keyword=model.keyword,
                    frequency=model.frequency,
                    metadata=model.meta_data,
                    created_at=model.created_at.isoformat()
                    if model.created_at
                    else "",
                )
                for model in models
            ]

        except Exception as e:
            raise DatabaseError(
                message="Failed to get analysis results by scraping result ID",
                error_code="ANALYSIS_RESULT_GET_BY_SCRAPING_ID_ERROR",
                details={
                    "error": str(e),
                    "scraping_result_id": str(scraping_result_id),
                },
            ) from e

    async def get_unprocessed_scraping_ids(
        self, limit: int, analysis_type: AnalysisType
    ) -> List[UUID]:
        """Get IDs of unprocessed scraping results."""
        try:
            # Subquery to find scraping IDs that already have this analysis type
            processed_ids_subquery = (
                select(AnalysisResultModel.scraping_result_id)
                .where(AnalysisResultModel.analysis_type == analysis_type)
                .distinct()
            )

            # Get scraping IDs that are not in the processed list
            # Use ~ (NOT) operator with .in_()
            stmt = (
                select(ScrapingResultModel.id)
                .where(
                    ~ScrapingResultModel.id.in_(
                        processed_ids_subquery
                    )
                )
                .limit(limit)
            )

            result = await self._session.execute(stmt)
            ids = result.scalars().all()

            return list(ids)

        except Exception as e:
            raise DatabaseError(
                message="Failed to get unprocessed scraping IDs",
                error_code="ANALYSIS_GET_UNPROCESSED_ERROR",
                details={
                    "error": str(e),
                    "limit": limit,
                    "analysis_type": analysis_type.value,
                },
            ) from e

