"""Data Transfer Objects for analysis results."""

from datetime import datetime
from uuid import UUID
from typing import Dict, Any, Optional

from shared.types.enums import AnalysisType


class AnalysisResultDTO:
    """DTO for analysis results."""

    def __init__(
        self,
        id: UUID,
        scraping_result_id: UUID,
        analysis_type: AnalysisType,
        keyword: Optional[str],
        frequency: int,
        metadata: Optional[Dict[str, Any]],
        created_at: datetime,
    ) -> None:
        """Initialize analysis result DTO.

        Args:
            id: Unique identifier
            scraping_result_id: ID of the scraped result being analyzed
            analysis_type: Type of analysis performed
            keyword: Keyword analyzed (if applicable)
            frequency: Frequency count (if applicable)
            metadata: Additional analysis metadata
            created_at: Timestamp when analysis was performed
        """
        self.id = id
        self.scraping_result_id = scraping_result_id
        self.analysis_type = analysis_type
        self.keyword = keyword
        self.frequency = frequency
        self.metadata = metadata
        self.created_at = created_at

