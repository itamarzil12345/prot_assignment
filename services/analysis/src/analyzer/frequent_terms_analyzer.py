"""Frequent terms analyzer implementation.

This analyzer aggregates KEYWORD_FREQUENCY records across all documents
to identify the globally most frequent terms and stores them as FREQUENT_TERMS
analysis results.
"""

import uuid
from datetime import datetime, timezone
from typing import List

from services.analysis.src.analyzer.analyzer_interface import AnalyzerInterface
from services.analysis.src.models.analysis_result_dto import AnalysisResultDTO
from services.analysis.src.errors.analysis_errors import AnalysisError
from services.analysis.src.repository.analysis_repository_interface import (
    AnalysisRepositoryInterface,
)
from shared.logging.logger_interface import LoggerInterface
from shared.types.enums import AnalysisType
from shared.constants import Limits


class FrequentTermsAnalyzer(AnalyzerInterface):
    """Analyzer for identifying globally most frequent terms across all documents.
    
    This analyzer aggregates KEYWORD_FREQUENCY records to find the top N
    most frequently occurring terms across all documents. Unlike KEYWORD_FREQUENCY
    which stores per-document counts, FREQUENT_TERMS stores global aggregated statistics.
    """

    def __init__(
        self, logger: LoggerInterface, analysis_repo: AnalysisRepositoryInterface
    ) -> None:
        """Initialize frequent terms analyzer.
        
        Args:
            logger: Logger instance for logging operations
            analysis_repo: Repository for accessing analysis results
        """
        self._logger = logger
        self._analysis_repo = analysis_repo
        self._limit = Limits.MAX_KEYWORD_FREQUENCY_RESULTS  # Top N terms to store

    async def get_analysis_type(self) -> str:
        """Get the type of analysis performed."""
        return AnalysisType.FREQUENT_TERMS.value

    async def analyze(
        self, scraping_result=None  # Not used for global aggregation
    ) -> List[AnalysisResultDTO]:
        """Analyze all KEYWORD_FREQUENCY records to find globally most frequent terms.
        
        This method aggregates KEYWORD_FREQUENCY records across all documents
        and creates FREQUENT_TERMS analysis results for the top N terms.
        
        Args:
            scraping_result: Not used (this is a global aggregation analysis)
        
        Returns:
            List of frequent terms analysis results
        
        Raises:
            AnalysisError: If analysis fails
        """
        try:
            await self._logger.debug("Starting frequent terms analysis (global aggregation)")

            # Get aggregated most frequent terms from KEYWORD_FREQUENCY records
            aggregated_terms = await self._analysis_repo.get_most_frequent_terms(
                limit=self._limit, analysis_type=AnalysisType.KEYWORD_FREQUENCY
            )

            # Create analysis results
            results: List[AnalysisResultDTO] = []

            for term_data in aggregated_terms:
                result = AnalysisResultDTO(
                    id=uuid.uuid4(),
                    scraping_result_id=None,  # Global aggregation, not tied to a specific document
                    analysis_type=AnalysisType.FREQUENT_TERMS,
                    keyword=term_data["keyword"],
                    frequency=term_data["total_frequency"],  # Total frequency across all documents
                    metadata={
                        "document_count": term_data["document_count"],
                        "aggregated_from": AnalysisType.KEYWORD_FREQUENCY.value,
                        "rank": len(results) + 1,
                    },
                    created_at=datetime.now(timezone.utc),
                )
                results.append(result)

            await self._logger.debug(
                f"Frequent terms analysis completed: {len(results)} terms identified"
            )

            return results

        except Exception as e:
            error_msg = f"Frequent terms analysis failed: {str(e)}"
            await self._logger.error(error_msg, extra={"error": str(e)})
            raise AnalysisError(
                message=error_msg,
                error_code="FREQUENT_TERMS_FAILED",
                details={"error": str(e)},
            ) from e

