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
        self._max_ngram_size = Limits.MAX_NGRAM_SIZE
        self._min_ngram_size = Limits.MIN_NGRAM_SIZE
        self._max_stop_word_ratio = Limits.MAX_STOP_WORD_RATIO_IN_NGRAM

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
        """Extract keyword frequencies from text, including phrases (n-grams).

        Extracts:
        1. Individual words (filtered stop words and short words)
        2. Multi-word phrases (n-grams) from bigrams up to max_ngram_size

        Args:
            text: Text to analyze

        Returns:
            Dictionary mapping keywords/phrases to frequencies
        """
        counter = Counter()

        # Extract words using regex with word boundaries
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())

        # 1. Extract individual words (filter stop words and short words)
        filtered_words = [
            word for word in words
            if len(word) >= self._min_word_length
            and word not in self._stop_words
        ]
        counter.update(filtered_words)

        # 2. Extract n-grams (phrases) from bigrams to max_ngram_size
        for n in range(self._min_ngram_size, self._max_ngram_size + 1):
            ngrams = self._extract_ngrams(words, n)
            counter.update(ngrams)

        # Return top N most frequent keywords/phrases
        top_keywords = dict(
            counter.most_common(Limits.MAX_KEYWORD_FREQUENCY_RESULTS)
        )

        return top_keywords

    def _extract_ngrams(self, words: List[str], n: int) -> List[str]:
        """Extract n-grams (phrases) from a list of words.

        Args:
            words: List of words (already lowercased)
            n: Size of n-gram (2 = bigram, 3 = trigram, etc.)

        Returns:
            List of valid n-grams (phrases) as strings
        """
        ngrams = []
        
        # Generate all possible n-grams
        for i in range(len(words) - n + 1):
            ngram_words = words[i:i + n]
            ngram_phrase = " ".join(ngram_words)
            
            # Filter n-grams based on quality criteria
            if self._is_valid_ngram(ngram_words):
                ngrams.append(ngram_phrase)
        
        return ngrams

    def _is_valid_ngram(self, words: List[str]) -> bool:
        """Check if an n-gram is valid based on stop word ratio and word length.

        Args:
            words: List of words in the n-gram

        Returns:
            True if n-gram is valid, False otherwise
        """
        if not words:
            return False
        
        # Count stop words and non-stop words
        stop_word_count = sum(1 for word in words if word in self._stop_words)
        non_stop_words = [word for word in words if word not in self._stop_words]
        
        # Check stop word ratio
        stop_word_ratio = stop_word_count / len(words)
        if stop_word_ratio > self._max_stop_word_ratio:
            return False
        
        # Must have at least one non-stop word that meets minimum length
        valid_words = [
            word for word in non_stop_words
            if len(word) >= self._min_word_length
        ]
        if not valid_words:
            return False
        
        # Don't allow n-grams that start or end with only stop words
        # (unless they have valid content words in between)
        if words[0] in self._stop_words and words[-1] in self._stop_words:
            # Allow if there's at least one valid word in the middle
            if len(valid_words) == 0:
                return False
        
        return True

