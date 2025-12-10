"""Repository interface for scraping results."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
from uuid import UUID

from shared.errors import DatabaseError, NotFoundError
from shared.types.enums import SourceType


class ScrapingResultDTO:
    """Data Transfer Object for scraping results."""

    def __init__(
        self,
        id: UUID,
        source_type: SourceType,
        external_id: str,
        title: str,
        data: dict,
        link: str,
        scraped_at: datetime,
    ) -> None:
        """Initialize scraping result DTO."""
        self.id = id
        self.source_type = source_type
        self.external_id = external_id
        self.title = title
        self.data = data
        self.link = link
        self.scraped_at = scraped_at


class ScrapingRepositoryInterface(ABC):
    """Interface for scraping result repository."""

    @abstractmethod
    async def create(self, result: ScrapingResultDTO) -> UUID:
        """Create a new scraping result.

        Args:
            result: Scraping result DTO

        Returns:
            UUID of created result

        Raises:
            DatabaseError: If database operation fails
        """
        pass

    @abstractmethod
    async def get_by_id(self, result_id: UUID) -> Optional[ScrapingResultDTO]:
        """Get scraping result by ID.

        Args:
            result_id: UUID of the result

        Returns:
            ScrapingResultDTO if found, None otherwise

        Raises:
            DatabaseError: If database operation fails
        """
        pass

    @abstractmethod
    async def get_by_external_id(
        self, external_id: str, source_type: SourceType
    ) -> Optional[ScrapingResultDTO]:
        """Get scraping result by external ID and source type.

        Args:
            external_id: External ID from source system
            source_type: Type of source

        Returns:
            ScrapingResultDTO if found, None otherwise

        Raises:
            DatabaseError: If database operation fails
        """
        pass

    @abstractmethod
    async def exists_by_external_id(
        self, external_id: str, source_type: SourceType
    ) -> bool:
        """Check if scraping result exists by external ID.

        Args:
            external_id: External ID from source system
            source_type: Type of source

        Returns:
            True if exists, False otherwise

        Raises:
            DatabaseError: If database operation fails
        """
        pass

