"""Frequency analyzer implementation."""

import uuid
from datetime import datetime, timezone
from typing import List, Dict
from collections import Counter

from services.analysis.src.analyzer.analyzer_interface import AnalyzerInterface
from services.analysis.src.models.analysis_result_dto import AnalysisResultDTO
from services.analysis.src.errors.analysis_errors import FrequencyAnalysisError
from services.scraper.src.models.scraping_result_dto import ScrapingResultDTO
from shared.constants import Limits
from shared.logging.logger_interface import LoggerInterface
from shared.types.enums import AnalysisType


class FrequencyAnalyzer(AnalyzerInterface):
    """Analyzer for counting term frequencies in scraped data."""

    def __init__(self, logger: LoggerInterface) -> None:
        """Initialize frequency analyzer.

        Args:
            logger: Logger instance for logging operations
        """
        self._logger = logger

    async def get_analysis_type(self) -> str:
        """Get the type of analysis performed."""
        return "FREQUENCY_ANALYSIS"

    async def analyze(
        self, scraping_result: ScrapingResultDTO
    ) -> List[AnalysisResultDTO]:
        """Analyze scraping result for term frequencies.

        Args:
            scraping_result: Scraped data to analyze

        Returns:
            List of frequency analysis results

        Raises:
            FrequencyAnalysisError: If analysis fails
        """
        try:
            await self._logger.debug(
                f"Starting frequency analysis for scraping result: {scraping_result.id}"
            )

            # Extract all terms from the data
            terms = self._extract_terms(scraping_result)

            # Count frequencies
            term_counts = Counter(terms)

            # Create analysis results
            results: List[AnalysisResultDTO] = []

            # Get top terms
            top_terms = term_counts.most_common(Limits.ANALYSIS_BATCH_SIZE)

            for term, frequency in top_terms:
                result = AnalysisResultDTO(
                    id=uuid.uuid4(),
                    scraping_result_id=scraping_result.id,
                    analysis_type=AnalysisType.KEYWORD_FREQUENCY,  # Using same type
                    keyword=term,
                    frequency=frequency,
                    metadata={
                        "source_type": scraping_result.source_type.value,
                        "title": scraping_result.title,
                    },
                    created_at=datetime.now(timezone.utc),
                )
                results.append(result)

            await self._logger.debug(
                f"Frequency analysis completed: {len(results)} terms found"
            )

            return results

        except Exception as e:
            error_msg = f"Frequency analysis failed: {str(e)}"
            await self._logger.error(error_msg, extra={"error": str(e)})
            raise FrequencyAnalysisError(
                message=error_msg,
                error_code="FREQUENCY_ANALYSIS_FAILED",
                details={
                    "scraping_result_id": str(scraping_result.id),
                    "error": str(e),
                },
            ) from e

    def _extract_terms(self, scraping_result: ScrapingResultDTO) -> List[str]:
        """Extract terms from scraping result for frequency counting.

        Args:
            scraping_result: Scraping result to extract terms from

        Returns:
            List of terms
        """
        terms: List[str] = []

        # Add title words
        if scraping_result.title:
            terms.extend(scraping_result.title.lower().split())

        # Extract terms from data
        if scraping_result.data:
            terms.extend(self._extract_terms_from_dict(scraping_result.data))

        return terms

    def _extract_terms_from_dict(self, data: dict) -> List[str]:
        """Recursively extract terms from dictionary.

        Args:
            data: Dictionary to extract terms from

        Returns:
            List of terms
        """
        terms: List[str] = []

        for key, value in data.items():
            if isinstance(value, str):
                terms.extend(value.lower().split())
            elif isinstance(value, dict):
                terms.extend(self._extract_terms_from_dict(value))
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, str):
                        terms.extend(item.lower().split())
                    elif isinstance(item, dict):
                        terms.extend(self._extract_terms_from_dict(item))

        return terms

