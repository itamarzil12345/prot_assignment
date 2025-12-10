"""Repository interface for scraping results (API service)."""

from abc import ABC, abstractmethod
from typing import Optional, List
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
        scraped_at: str,
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
    async def list_all(
        self, limit: int, offset: int, source_type: Optional[SourceType] = None
    ) -> List[ScrapingResultDTO]:
        """List scraping results with pagination.

        Args:
            limit: Maximum number of results
            offset: Number of results to skip
            source_type: Optional filter by source type

        Returns:
            List of scraping result DTOs

        Raises:
            DatabaseError: If database operation fails
        """
        pass

    @abstractmethod
    async def update(self, result_id: UUID, updates: dict) -> ScrapingResultDTO:
        """Update a scraping result.

        Args:
            result_id: UUID of the result to update
            updates: Dictionary of fields to update

        Returns:
            Updated ScrapingResultDTO

        Raises:
            NotFoundError: If result not found
            DatabaseError: If database operation fails
        """
        pass

    @abstractmethod
    async def delete(self, result_id: UUID) -> None:
        """Delete a scraping result.

        Args:
            result_id: UUID of the result to delete

        Raises:
            NotFoundError: If result not found
            DatabaseError: If database operation fails
        """
        pass

