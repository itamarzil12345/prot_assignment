"""Keyword analyzer implementation."""

import re
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Set
from collections import Counter

from services.analysis.src.analyzer.analyzer_interface import AnalyzerInterface
from services.analysis.src.models.analysis_result_dto import AnalysisResultDTO
from services.analysis.src.errors.analysis_errors import KeywordAnalysisError
from services.scraper.src.models.scraping_result_dto import ScrapingResultDTO
from shared.constants import Limits
from shared.logging.logger_interface import LoggerInterface
from shared.types.enums import AnalysisType


class KeywordAnalyzer(AnalyzerInterface):
    """Analyzer for extracting and counting keyword frequencies."""

    # Common medical/clinical keywords to look for
    MEDICAL_KEYWORDS = {
        "treatment", "patient", "clinical", "dose", "dosage", "side effect",
        "adverse", "efficacy", "safety", "trial", "study", "condition",
        "disease", "therapy", "medication", "drug", "indication",
        "contraindication", "interaction", "pharmacokinetics",
        "pharmacodynamics", "metabolism", "excretion",
    }

    def __init__(self, logger: LoggerInterface) -> None:
        """Initialize keyword analyzer.

        Args:
            logger: Logger instance for logging operations
        """
        self._logger = logger
        self._min_word_length = 3

    async def get_analysis_type(self) -> str:
        """Get the type of analysis performed."""
        return AnalysisType.KEYWORD_FREQUENCY.value

    async def analyze(
        self, scraping_result: ScrapingResultDTO
    ) -> List[AnalysisResultDTO]:
        """Analyze scraping result for keyword frequencies.

        Args:
            scraping_result: Scraped data to analyze

        Returns:
            List of keyword frequency analysis results

        Raises:
            KeywordAnalysisError: If analysis fails
        """
        try:
            await self._logger.debug(
                f"Starting keyword analysis for scraping result: {scraping_result.id}"
            )

            # Extract text from scraping result data
            text = self._extract_text(scraping_result)

            # Extract keywords and count frequencies
            keyword_counts = self._extract_keyword_frequencies(text)

            # Create analysis results
            results: List[AnalysisResultDTO] = []

            for keyword, frequency in keyword_counts.items():
                result = AnalysisResultDTO(
                    id=uuid.uuid4(),
                    scraping_result_id=scraping_result.id,
                    analysis_type=AnalysisType.KEYWORD_FREQUENCY,
                    keyword=keyword,
                    frequency=frequency,
                    metadata={
                        "source_type": scraping_result.source_type.value,
                        "title": scraping_result.title,
                    },
                    created_at=datetime.now(timezone.utc),
                )
                results.append(result)

            await self._logger.debug(
                f"Keyword analysis completed: {len(results)} keywords found"
            )

            return results

        except Exception as e:
            error_msg = f"Keyword analysis failed: {str(e)}"
            await self._logger.error(error_msg, extra={"error": str(e)})
            raise KeywordAnalysisError(
                message=error_msg,
                error_code="KEYWORD_ANALYSIS_FAILED",
                details={"scraping_result_id": str(scraping_result.id), "error": str(e)},
            ) from e

    def _extract_text(self, scraping_result: ScrapingResultDTO) -> str:
        """Extract text content from scraping result.

        Args:
            scraping_result: Scraping result to extract text from

        Returns:
            Combined text content
        """
        text_parts: List[str] = []

        # Add title
        if scraping_result.title:
            text_parts.append(scraping_result.title)

        # Extract text from data dictionary
        if scraping_result.data:
            text_parts.extend(self._extract_text_from_dict(scraping_result.data))

        return " ".join(text_parts)

    def _extract_text_from_dict(self, data: dict) -> List[str]:
        """Recursively extract text from dictionary.

        Args:
            data: Dictionary to extract text from

        Returns:
            List of text strings
        """
        text_parts: List[str] = []

        for key, value in data.items():
            if isinstance(value, str):
                text_parts.append(value)
            elif isinstance(value, dict):
                text_parts.extend(self._extract_text_from_dict(value))
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, str):
                        text_parts.append(item)
                    elif isinstance(item, dict):
                        text_parts.extend(self._extract_text_from_dict(item))

        return text_parts

    def _extract_keyword_frequencies(self, text: str) -> Dict[str, int]:
        """Extract keyword frequencies from text.

        Args:
            text: Text to analyze

        Returns:
            Dictionary mapping keywords to frequencies
        """
        # Convert to lowercase and split into words
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())

        # Filter words by length and medical keywords
        filtered_words = [
            word for word in words
            if len(word) >= self._min_word_length
            and word in self.MEDICAL_KEYWORDS
        ]

        # Count frequencies
        counter = Counter(filtered_words)

        # Return top keywords (limit to avoid too many results)
        top_keywords = dict(counter.most_common(Limits.ANALYSIS_BATCH_SIZE))

        return top_keywords

