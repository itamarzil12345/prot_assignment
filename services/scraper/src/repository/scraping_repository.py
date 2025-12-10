"""Repository implementation for scraping results."""

from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from services.api.src.database.models import ScrapingResultModel
from services.scraper.src.repository.scraping_repository_interface import (
    ScrapingRepositoryInterface,
    ScrapingResultDTO,
)
from shared.errors import DatabaseError
from shared.types.enums import SourceType


class ScrapingRepository(ScrapingRepositoryInterface):
    """SQLAlchemy implementation of scraping repository."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize repository with database session.

        Args:
            session: Async database session
        """
        self._session = session

    async def create(self, result: ScrapingResultDTO) -> UUID:
        """Create a new scraping result."""
        try:
            model = ScrapingResultModel(
                id=result.id,
                source_type=result.source_type,
                external_id=result.external_id,
                title=result.title,
                data=result.data,
                link=result.link,
                scraped_at=result.scraped_at,
            )

            self._session.add(model)
            await self._session.flush()
            return model.id

        except Exception as e:
            raise DatabaseError(
                message="Failed to create scraping result",
                error_code="SCRAPING_RESULT_CREATE_ERROR",
                details={"error": str(e)},
            ) from e

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
                scraped_at=model.scraped_at,
            )

        except Exception as e:
            raise DatabaseError(
                message="Failed to get scraping result by ID",
                error_code="SCRAPING_RESULT_GET_ERROR",
                details={"error": str(e), "result_id": str(result_id)},
            ) from e

    async def get_by_external_id(
        self, external_id: str, source_type: SourceType
    ) -> Optional[ScrapingResultDTO]:
        """Get scraping result by external ID."""
        try:
            stmt = select(ScrapingResultModel).where(
                ScrapingResultModel.external_id == external_id,
                ScrapingResultModel.source_type == source_type,
            )
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
                scraped_at=model.scraped_at,
            )

        except Exception as e:
            raise DatabaseError(
                message="Failed to get scraping result by external ID",
                error_code="SCRAPING_RESULT_GET_BY_EXTERNAL_ID_ERROR",
                details={
                    "error": str(e),
                    "external_id": external_id,
                    "source_type": source_type.value,
                },
            ) from e

    async def exists_by_external_id(
        self, external_id: str, source_type: SourceType
    ) -> bool:
        """Check if scraping result exists."""
        try:
            stmt = select(ScrapingResultModel.id).where(
                ScrapingResultModel.external_id == external_id,
                ScrapingResultModel.source_type == source_type,
            )
            result = await self._session.execute(stmt)
            return result.scalar_one_or_none() is not None

        except Exception as e:
            raise DatabaseError(
                message="Failed to check scraping result existence",
                error_code="SCRAPING_RESULT_EXISTS_ERROR",
                details={
                    "error": str(e),
                    "external_id": external_id,
                    "source_type": source_type.value,
                },
            ) from e

