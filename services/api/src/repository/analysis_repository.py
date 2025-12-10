"""Repository implementation for analysis results (API service)."""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from services.api.src.database.models import AnalysisResultModel
from services.api.src.repository.analysis_repository_interface import (
    AnalysisRepositoryInterface,
    AnalysisResultDTO,
)
from shared.errors import DatabaseError, NotFoundError
from shared.types.enums import AnalysisType


class AnalysisRepository(AnalysisRepositoryInterface):
    """SQLAlchemy implementation of analysis repository for API."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize repository with database session.

        Args:
            session: Async database session
        """
        self._session = session

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
                created_at=model.created_at.isoformat() if model.created_at else "",
            )

        except Exception as e:
            raise DatabaseError(
                message="Failed to get analysis result by ID",
                error_code="ANALYSIS_RESULT_GET_ERROR",
                details={"error": str(e), "result_id": str(result_id)},
            ) from e

    async def list_all(
        self,
        limit: int,
        offset: int,
        analysis_type: Optional[AnalysisType] = None,
        scraping_result_id: Optional[UUID] = None,
    ) -> List[AnalysisResultDTO]:
        """List analysis results with pagination."""
        try:
            stmt = select(AnalysisResultModel).limit(limit).offset(offset)

            if analysis_type:
                stmt = stmt.where(AnalysisResultModel.analysis_type == analysis_type)

            if scraping_result_id:
                stmt = stmt.where(
                    AnalysisResultModel.scraping_result_id == scraping_result_id
                )

            stmt = stmt.order_by(AnalysisResultModel.created_at.desc())

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
                message="Failed to list analysis results",
                error_code="ANALYSIS_RESULT_LIST_ERROR",
                details={"error": str(e), "limit": limit, "offset": offset},
            ) from e

    async def update(self, result_id: UUID, updates: dict) -> AnalysisResultDTO:
        """Update an analysis result."""
        try:
            # Check if exists first
            existing = await self.get_by_id(result_id)
            if not existing:
                raise NotFoundError(
                    message="Analysis result not found",
                    error_code="ANALYSIS_RESULT_NOT_FOUND",
                    details={"result_id": str(result_id)},
                )

            stmt = (
                update(AnalysisResultModel)
                .where(AnalysisResultModel.id == result_id)
                .values(**updates)
            )

            await self._session.execute(stmt)
            await self._session.flush()

            # Return updated entity
            updated = await self.get_by_id(result_id)
            if not updated:
                raise NotFoundError(
                    message="Analysis result not found after update",
                    error_code="ANALYSIS_RESULT_NOT_FOUND",
                    details={"result_id": str(result_id)},
                )

            return updated

        except NotFoundError:
            raise
        except Exception as e:
            raise DatabaseError(
                message="Failed to update analysis result",
                error_code="ANALYSIS_RESULT_UPDATE_ERROR",
                details={"error": str(e), "result_id": str(result_id)},
            ) from e

    async def delete(self, result_id: UUID) -> None:
        """Delete an analysis result."""
        try:
            # Check if exists first
            existing = await self.get_by_id(result_id)
            if not existing:
                raise NotFoundError(
                    message="Analysis result not found",
                    error_code="ANALYSIS_RESULT_NOT_FOUND",
                    details={"result_id": str(result_id)},
                )

            stmt = delete(AnalysisResultModel).where(
                AnalysisResultModel.id == result_id
            )
            await self._session.execute(stmt)
            await self._session.flush()

        except NotFoundError:
            raise
        except Exception as e:
            raise DatabaseError(
                message="Failed to delete analysis result",
                error_code="ANALYSIS_RESULT_DELETE_ERROR",
                details={"error": str(e), "result_id": str(result_id)},
            ) from e

