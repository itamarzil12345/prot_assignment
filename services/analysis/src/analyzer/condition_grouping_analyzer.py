"""Condition grouping analyzer implementation."""

import uuid
import re
from datetime import datetime, timezone
from typing import List, Dict, Set
from collections import defaultdict

from services.analysis.src.analyzer.analyzer_interface import AnalyzerInterface
from services.analysis.src.models.analysis_result_dto import AnalysisResultDTO
from services.analysis.src.errors.analysis_errors import AnalysisError
from services.scraper.src.models.scraping_result_dto import ScrapingResultDTO
from shared.logging.logger_interface import LoggerInterface
from shared.types.enums import AnalysisType

# Common medical conditions
COMMON_CONDITIONS = {
    "diabetes", "hypertension", "cancer", "arthritis", "asthma",
    "depression", "anxiety", "heart disease", "stroke", "migraine",
    "epilepsy", "parkinson", "alzheimer", "osteoporosis", "obesity",
    "insomnia", "pain", "infection", "inflammation", "fever",
}


class ConditionGroupingAnalyzer(AnalyzerInterface):
    """Analyzer for grouping data by medical conditions."""

    def __init__(self, logger: LoggerInterface) -> None:
        """Initialize condition grouping analyzer.

        Args:
            logger: Logger instance for logging operations
        """
        self._logger = logger

    async def get_analysis_type(self) -> str:
        """Get the type of analysis performed."""
        return AnalysisType.CONDITION_GROUPING.value

    async def analyze(
        self, scraping_result: ScrapingResultDTO
    ) -> List[AnalysisResultDTO]:
        """Analyze scraping result for medical conditions.

        Args:
            scraping_result: Scraped data to analyze

        Returns:
            List of condition grouping analysis results

        Raises:
            AnalysisError: If analysis fails
        """
        try:
            await self._logger.debug(
                f"Starting condition grouping analysis for: {scraping_result.id}"
            )

            # Extract text
            text = self._extract_text(scraping_result).lower()

            # Find matching conditions
            found_conditions: Set[str] = set()

            for condition in COMMON_CONDITIONS:
                # Use word boundary matching
                pattern = r'\b' + re.escape(condition) + r'\b'
                if re.search(pattern, text, re.IGNORECASE):
                    found_conditions.add(condition)

            # Create analysis results
            results: List[AnalysisResultDTO] = []

            for condition in found_conditions:
                result = AnalysisResultDTO(
                    id=uuid.uuid4(),
                    scraping_result_id=scraping_result.id,
                    analysis_type=AnalysisType.CONDITION_GROUPING,
                    keyword=condition,
                    frequency=1,  # Count as 1 for grouping
                    metadata={
                        "source_type": scraping_result.source_type.value,
                        "title": scraping_result.title,
                        "grouped_by": "condition",
                    },
                    created_at=datetime.now(timezone.utc),
                )
                results.append(result)

            await self._logger.debug(
                f"Condition grouping completed: {len(results)} conditions found"
            )

            return results

        except Exception as e:
            error_msg = f"Condition grouping analysis failed: {str(e)}"
            await self._logger.error(error_msg, extra={"error": str(e)})
            raise AnalysisError(
                message=error_msg,
                error_code="CONDITION_GROUPING_FAILED",
                details={
                    "scraping_result_id": str(scraping_result.id),
                    "error": str(e),
                },
            ) from e

    def _extract_text(self, scraping_result: ScrapingResultDTO) -> str:
        """Extract text content from scraping result.

        Args:
            scraping_result: Scraping result to extract text from

        Returns:
            Combined text content
        """
        text_parts: List[str] = []

        if scraping_result.title:
            text_parts.append(scraping_result.title)

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

