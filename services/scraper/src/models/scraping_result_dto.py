"""Data Transfer Objects for scraping results."""

from datetime import datetime
from uuid import UUID
from typing import Dict, Any

from shared.types.enums import SourceType


class ScrapingResultDTO:
    """DTO for scraping results."""

    def __init__(
        self,
        id: UUID,
        source_type: SourceType,
        external_id: str,
        title: str,
        data: Dict[str, Any],
        link: str,
        scraped_at: datetime,
    ) -> None:
        """Initialize scraping result DTO.

        Args:
            id: Unique identifier
            source_type: Type of data source
            external_id: External ID from source system
            title: Title of the record
            data: Raw data as dictionary
            link: URL link to the source
            scraped_at: Timestamp when data was scraped
        """
        self.id = id
        self.source_type = source_type
        self.external_id = external_id
        self.title = title
        self.data = data
        self.link = link
        self.scraped_at = scraped_at

