"""Repository interface for analysis results (API service)."""

from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from shared.errors import DatabaseError, NotFoundError
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
    async def list_all(
        self,
        limit: int,
        offset: int,
        analysis_type: Optional[AnalysisType] = None,
        scraping_result_id: Optional[UUID] = None,
        keyword: Optional[str] = None,
    ) -> List[AnalysisResultDTO]:
        """List analysis results with pagination.

        Args:
            limit: Maximum number of results
            offset: Number of results to skip
            analysis_type: Optional filter by analysis type
            scraping_result_id: Optional filter by scraping result ID
            keyword: Optional filter by keyword (case-insensitive partial match)

        Returns:
            List of analysis result DTOs

        Raises:
            DatabaseError: If database operation fails
        """
        pass

    @abstractmethod
    async def count_all(
        self,
        analysis_type: Optional[AnalysisType] = None,
        scraping_result_id: Optional[UUID] = None,
        keyword: Optional[str] = None,
    ) -> int:
        """Count total analysis results matching filters.

        Args:
            analysis_type: Optional filter by analysis type
            scraping_result_id: Optional filter by scraping result ID
            keyword: Optional filter by keyword (case-insensitive partial match)

        Returns:
            Total count of matching results

        Raises:
            DatabaseError: If database operation fails
        """
        pass

    @abstractmethod
    async def get_most_frequent_terms(
        self,
        limit: int,
        analysis_type: Optional[AnalysisType] = None,
    ) -> List[dict]:
        """Get most frequent terms across all analysis results.

        Args:
            limit: Maximum number of terms to return
            analysis_type: Optional filter by analysis type

        Returns:
            List of dictionaries with 'keyword' and 'total_frequency' keys,
            ordered by total frequency descending

        Raises:
            DatabaseError: If database operation fails
        """
        pass

    @abstractmethod
    async def update(self, result_id: UUID, updates: dict) -> AnalysisResultDTO:
        """Update an analysis result.

        Args:
            result_id: UUID of the result to update
            updates: Dictionary of fields to update

        Returns:
            Updated AnalysisResultDTO

        Raises:
            NotFoundError: If result not found
            DatabaseError: If database operation fails
        """
        pass

    @abstractmethod
    async def delete(self, result_id: UUID) -> None:
        """Delete an analysis result.

        Args:
            result_id: UUID of the result to delete

        Raises:
            NotFoundError: If result not found
            DatabaseError: If database operation fails
        """
        pass

