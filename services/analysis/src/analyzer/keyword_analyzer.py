"""Keyword analyzer implementation."""

import re
import uuid
from datetime import datetime, timezone
from typing import List, Dict
from collections import Counter

from services.analysis.src.analyzer.analyzer_interface import AnalyzerInterface
from services.analysis.src.models.analysis_result_dto import AnalysisResultDTO
from services.analysis.src.errors.analysis_errors import KeywordAnalysisError
from services.scraper.src.models.scraping_result_dto import ScrapingResultDTO
from shared.constants import Limits
from shared.logging.logger_interface import LoggerInterface
from shared.types.enums import AnalysisType
from shared.utils.stop_words import get_stop_words
from shared.utils.text_extractor import extract_all_text


class KeywordAnalyzer(AnalyzerInterface):
    """Analyzer for extracting and counting keyword frequencies from actual data."""

    def __init__(self, logger: LoggerInterface) -> None:
        """Initialize keyword analyzer.

        Args:
            logger: Logger instance for logging operations
        """
        self._logger = logger
        self._min_word_length = Limits.MIN_KEYWORD_LENGTH
        self._stop_words = get_stop_words()

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

            # Extract all text from scraping result using utility
            text_parts: List[str] = []
            if scraping_result.title:
                text_parts.append(scraping_result.title)
            if scraping_result.data:
                text_parts.append(extract_all_text(scraping_result.data))
            text = " ".join(text_parts)

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

    def _extract_keyword_frequencies(self, text: str) -> Dict[str, int]:
        """Extract keyword frequencies from text.

        Extracts all words from text, filters stop words and short words,
        then counts frequencies to find most common terms.

        Args:
            text: Text to analyze

        Returns:
            Dictionary mapping keywords to frequencies
        """
        # Extract words using regex with word boundaries
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())

        # Filter words: remove stop words and short words
        filtered_words = [
            word for word in words
            if len(word) >= self._min_word_length
            and word not in self._stop_words
        ]

        # Count frequencies using Counter
        counter = Counter(filtered_words)

        # Return top N most frequent keywords
        top_keywords = dict(
            counter.most_common(Limits.MAX_KEYWORD_FREQUENCY_RESULTS)
        )

        return top_keywords

