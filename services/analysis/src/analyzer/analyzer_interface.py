"""Interface for analyzers."""

from abc import ABC, abstractmethod
from typing import List

from services.analysis.src.models.analysis_result_dto import AnalysisResultDTO
from services.scraper.src.models.scraping_result_dto import ScrapingResultDTO


class AnalyzerInterface(ABC):
    """Abstract interface for analyzers."""

    @abstractmethod
    async def analyze(
        self, scraping_result: ScrapingResultDTO
    ) -> List[AnalysisResultDTO]:
        """Analyze a scraping result.

        Args:
            scraping_result: Scraped data to analyze

        Returns:
            List of analysis results

        Raises:
            AnalysisError: If analysis fails
        """
        pass

    @abstractmethod
    async def get_analysis_type(self) -> str:
        """Get the type of analysis performed.

        Returns:
            Analysis type name
        """
        pass

