"""Repository interface for analysis results."""

from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from shared.errors import DatabaseError
from shared.types.enums import AnalysisType


class AnalysisResultDTO:
    """Data Transfer Object for analysis results."""

    def __init__(
        self,
        id: UUID,
        scraping_result_id: UUID,
        analysis_type: AnalysisType,
        keyword: Optional[str],
        frequency: int,
        metadata: Optional[dict],
        created_at: str,
    ) -> None:
        """Initialize analysis result DTO."""
        self.id = id
        self.scraping_result_id = scraping_result_id
        self.analysis_type = analysis_type
        self.keyword = keyword
        self.frequency = frequency
        self.metadata = metadata
        self.created_at = created_at


class AnalysisRepositoryInterface(ABC):
    """Interface for analysis result repository."""

    @abstractmethod
    async def create(self, result: AnalysisResultDTO) -> UUID:
        """Create a new analysis result.

        Args:
            result: Analysis result DTO

        Returns:
            UUID of created result

        Raises:
            DatabaseError: If database operation fails
        """
        pass

    @abstractmethod
    async def create_batch(self, results: List[AnalysisResultDTO]) -> List[UUID]:
        """Create multiple analysis results in batch.

        Args:
            results: List of analysis result DTOs

        Returns:
            List of UUIDs of created results

        Raises:
            DatabaseError: If database operation fails
        """
        pass

    @abstractmethod
    async def get_by_id(self, result_id: UUID) -> Optional[AnalysisResultDTO]:
        """Get analysis result by ID.

        Args:
            result_id: UUID of the result

        Returns:
            AnalysisResultDTO if found, None otherwise

        Raises:
            DatabaseError: If database operation fails
        """
        pass

    @abstractmethod
    async def get_by_scraping_result_id(
        self, scraping_result_id: UUID
    ) -> List[AnalysisResultDTO]:
        """Get all analysis results for a scraping result.

        Args:
            scraping_result_id: UUID of the scraping result

        Returns:
            List of analysis result DTOs

        Raises:
            DatabaseError: If database operation fails
        """
        pass

    @abstractmethod
    async def get_unprocessed_scraping_ids(
        self, limit: int, analysis_type: AnalysisType
    ) -> List[UUID]:
        """Get IDs of scraping results not yet processed for analysis type.

        Args:
            limit: Maximum number of IDs to return
            analysis_type: Type of analysis to check

        Returns:
            List of scraping result UUIDs

        Raises:
            DatabaseError: If database operation fails
        """
        pass

