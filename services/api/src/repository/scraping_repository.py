"""Repository implementation for scraping results (API service)."""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from services.api.src.database.models import ScrapingResultModel
from services.api.src.repository.scraping_repository_interface import (
    ScrapingRepositoryInterface,
    ScrapingResultDTO,
)
from shared.errors import DatabaseError, NotFoundError
from shared.types.enums import SourceType


class ScrapingRepository(ScrapingRepositoryInterface):
    """SQLAlchemy implementation of scraping repository for API."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize repository with database session.

        Args:
            session: Async database session
        """
        self._session = session

    async def get_by_id(self, result_id: UUID) -> Optional[ScrapingResultDTO]:
        """Get scraping result by ID."""
        try:
            stmt = select(ScrapingResultModel).where(ScrapingResultModel.id == result_id)
            result = await self._session.execute(stmt)
            model = result.scalar_one_or_none()

            if not model:
                return None

            return ScrapingResultDTO(
                id=model.id,
                source_type=model.source_type,
                external_id=model.external_id,
                title=model.title,
                data=model.data,
                link=model.link,
                scraped_at=model.scraped_at.isoformat() if model.scraped_at else "",
            )

        except Exception as e:
            raise DatabaseError(
                message="Failed to get scraping result by ID",
                error_code="SCRAPING_RESULT_GET_ERROR",
                details={"error": str(e), "result_id": str(result_id)},
            ) from e

    async def list_all(
        self, limit: int, offset: int, source_type: Optional[SourceType] = None
    ) -> List[ScrapingResultDTO]:
        """List scraping results with pagination."""
        try:
            stmt = select(ScrapingResultModel).limit(limit).offset(offset)

            if source_type:
                stmt = stmt.where(ScrapingResultModel.source_type == source_type)

            stmt = stmt.order_by(ScrapingResultModel.scraped_at.desc())

            result = await self._session.execute(stmt)
            models = result.scalars().all()

            return [
                ScrapingResultDTO(
                    id=model.id,
                    source_type=model.source_type,
                    external_id=model.external_id,
                    title=model.title,
                    data=model.data,
                    link=model.link,
                    scraped_at=model.scraped_at.isoformat()
                    if model.scraped_at
                    else "",
                )
                for model in models
            ]

        except Exception as e:
            raise DatabaseError(
                message="Failed to list scraping results",
                error_code="SCRAPING_RESULT_LIST_ERROR",
                details={"error": str(e), "limit": limit, "offset": offset},
            ) from e

    async def update(self, result_id: UUID, updates: dict) -> ScrapingResultDTO:
        """Update a scraping result."""
        try:
            # Check if exists first
            existing = await self.get_by_id(result_id)
            if not existing:
                raise NotFoundError(
                    message="Scraping result not found",
                    error_code="SCRAPING_RESULT_NOT_FOUND",
                    details={"result_id": str(result_id)},
                )

            stmt = (
                update(ScrapingResultModel)
                .where(ScrapingResultModel.id == result_id)
                .values(**updates)
            )

            await self._session.execute(stmt)
            await self._session.flush()

            # Return updated entity
            updated = await self.get_by_id(result_id)
            if not updated:
                raise NotFoundError(
                    message="Scraping result not found after update",
                    error_code="SCRAPING_RESULT_NOT_FOUND",
                    details={"result_id": str(result_id)},
                )

            return updated

        except NotFoundError:
            raise
        except Exception as e:
            raise DatabaseError(
                message="Failed to update scraping result",
                error_code="SCRAPING_RESULT_UPDATE_ERROR",
                details={"error": str(e), "result_id": str(result_id)},
            ) from e

    async def delete(self, result_id: UUID) -> None:
        """Delete a scraping result."""
        try:
            # Check if exists first
            existing = await self.get_by_id(result_id)
            if not existing:
                raise NotFoundError(
                    message="Scraping result not found",
                    error_code="SCRAPING_RESULT_NOT_FOUND",
                    details={"result_id": str(result_id)},
                )

            stmt = delete(ScrapingResultModel).where(
                ScrapingResultModel.id == result_id
            )
            await self._session.execute(stmt)
            await self._session.flush()

        except NotFoundError:
            raise
        except Exception as e:
            raise DatabaseError(
                message="Failed to delete scraping result",
                error_code="SCRAPING_RESULT_DELETE_ERROR",
                details={"error": str(e), "result_id": str(result_id)},
            ) from e

