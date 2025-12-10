"""Condition grouping analyzer implementation."""

import uuid
from datetime import datetime, timezone
from typing import List, Set

from services.analysis.src.analyzer.analyzer_interface import AnalyzerInterface
from services.analysis.src.models.analysis_result_dto import AnalysisResultDTO
from services.analysis.src.errors.analysis_errors import AnalysisError
from services.scraper.src.models.scraping_result_dto import ScrapingResultDTO
from shared.logging.logger_interface import LoggerInterface
from shared.types.enums import AnalysisType, SourceType


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

        Extracts conditions from structured fields in the data.
        For ClinicalTrials: extracts from conditionsModule.conditions
        For FDA: extracts from indication fields if available

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

            # Extract conditions based on source type
            found_conditions: Set[str] = set()

            if scraping_result.source_type == SourceType.CLINICAL_TRIALS:
                found_conditions = self._extract_conditions_from_clinical_trials(
                    scraping_result
                )
            elif scraping_result.source_type == SourceType.FDA_DRUG_LABELS:
                found_conditions = self._extract_conditions_from_fda(
                    scraping_result
                )

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

    def _extract_conditions_from_clinical_trials(
        self, scraping_result: ScrapingResultDTO
    ) -> Set[str]:
        """Extract conditions from ClinicalTrials structured data.

        Args:
            scraping_result: Scraping result with ClinicalTrials data

        Returns:
            Set of condition strings found
        """
        conditions: Set[str] = set()

        if not scraping_result.data:
            return conditions

        # Extract from protocolSection.conditionsModule.conditions
        protocol_section = scraping_result.data.get("protocolSection", {})
        conditions_module = protocol_section.get("conditionsModule", {})

        # Extract conditions array
        conditions_list = conditions_module.get("conditions", [])
        if isinstance(conditions_list, list):
            for condition in conditions_list:
                if isinstance(condition, str) and condition.strip():
                    conditions.add(condition.strip())

        # Also extract from keywords if available
        keywords_list = conditions_module.get("keywords", [])
        if isinstance(keywords_list, list):
            for keyword in keywords_list:
                if isinstance(keyword, str) and keyword.strip():
                    conditions.add(keyword.strip())

        return conditions

    def _extract_conditions_from_fda(
        self, scraping_result: ScrapingResultDTO
    ) -> Set[str]:
        """Extract conditions from FDA drug label data.

        Args:
            scraping_result: Scraping result with FDA data

        Returns:
            Set of condition strings found
        """
        conditions: Set[str] = set()

        if not scraping_result.data:
            return conditions

        # FDA data structure varies, check common indication fields
        # Look for indication, indication_text, or similar fields
        data = scraping_result.data

        # Check for indication field
        indication = data.get("indication") or data.get("indication_text")
        if isinstance(indication, str) and indication.strip():
            conditions.add(indication.strip())

        # Check for indications array if available
        indications = data.get("indications")
        if isinstance(indications, list):
            for ind in indications:
                if isinstance(ind, str) and ind.strip():
                    conditions.add(ind.strip())

        # Note: FDA data structure may vary by API endpoint
        # This is a basic extraction that can be extended

        return conditions

