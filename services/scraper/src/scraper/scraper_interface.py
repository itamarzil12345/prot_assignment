"""Interface for scrapers."""

from abc import ABC, abstractmethod
from typing import List

from services.scraper.src.models.scraping_result_dto import ScrapingResultDTO


class ScraperInterface(ABC):
    """Abstract interface for scrapers."""

    @abstractmethod
    async def scrape(self) -> List[ScrapingResultDTO]:
        """Scrape data from the source.

        Returns:
            List of scraped results as DTOs

        Raises:
            ExternalServiceError: If scraping fails
        """
        pass

    @abstractmethod
    async def get_source_name(self) -> str:
        """Get the name of the data source.

        Returns:
            Source name
        """
        pass

