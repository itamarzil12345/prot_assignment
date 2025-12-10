"""Category grouping analyzer implementation."""

import uuid
from datetime import datetime, timezone
from typing import List, Set

from services.analysis.src.analyzer.analyzer_interface import AnalyzerInterface
from services.analysis.src.models.analysis_result_dto import AnalysisResultDTO
from services.analysis.src.errors.analysis_errors import AnalysisError
from services.scraper.src.models.scraping_result_dto import ScrapingResultDTO
from shared.logging.logger_interface import LoggerInterface
from shared.types.enums import AnalysisType, SourceType


class CategoryGroupingAnalyzer(AnalyzerInterface):
    """Analyzer for grouping data by categories (phase, study type, etc.)."""

    def __init__(self, logger: LoggerInterface) -> None:
        """Initialize category grouping analyzer.

        Args:
            logger: Logger instance for logging operations
        """
        self._logger = logger

    async def get_analysis_type(self) -> str:
        """Get the type of analysis performed."""
        return AnalysisType.CATEGORY_GROUPING.value

    async def analyze(
        self, scraping_result: ScrapingResultDTO
    ) -> List[AnalysisResultDTO]:
        """Analyze scraping result for categories.

        Extracts categories from structured fields in the data.
        For ClinicalTrials: extracts phase, study type, intervention types, etc.
        For FDA: extracts drug category, route of administration, etc.

        Args:
            scraping_result: Scraped data to analyze

        Returns:
            List of category grouping analysis results

        Raises:
            AnalysisError: If analysis fails
        """
        try:
            await self._logger.debug(
                f"Starting category grouping analysis for: {scraping_result.id}"
            )

            # Extract categories based on source type
            found_categories: Set[tuple[str, str]] = set()

            if scraping_result.source_type == SourceType.CLINICAL_TRIALS:
                found_categories = self._extract_categories_from_clinical_trials(
                    scraping_result
                )
            elif scraping_result.source_type == SourceType.FDA_DRUG_LABELS:
                found_categories = self._extract_categories_from_fda(
                    scraping_result
                )

            # Create analysis results
            results: List[AnalysisResultDTO] = []

            for category_value, category_type in found_categories:
                result = AnalysisResultDTO(
                    id=uuid.uuid4(),
                    scraping_result_id=scraping_result.id,
                    analysis_type=AnalysisType.CATEGORY_GROUPING,
                    keyword=category_value,
                    frequency=1,  # Count as 1 for grouping
                    metadata={
                        "source_type": scraping_result.source_type.value,
                        "title": scraping_result.title,
                        "grouped_by": "category",
                        "category_type": category_type,
                    },
                    created_at=datetime.now(timezone.utc),
                )
                results.append(result)

            await self._logger.debug(
                f"Category grouping completed: {len(results)} categories found"
            )

            return results

        except Exception as e:
            error_msg = f"Category grouping analysis failed: {str(e)}"
            await self._logger.error(error_msg, extra={"error": str(e)})
            raise AnalysisError(
                message=error_msg,
                error_code="CATEGORY_GROUPING_FAILED",
                details={
                    "scraping_result_id": str(scraping_result.id),
                    "error": str(e),
                },
            ) from e

    def _extract_categories_from_clinical_trials(
        self, scraping_result: ScrapingResultDTO
    ) -> Set[tuple[str, str]]:
        """Extract categories from ClinicalTrials structured data.

        Args:
            scraping_result: Scraping result with ClinicalTrials data

        Returns:
            Set of tuples (category_value, category_type)
        """
        categories: Set[tuple[str, str]] = set()

        if not scraping_result.data:
            return categories

        protocol_section = scraping_result.data.get("protocolSection", {})

        # Extract study phase
        design_module = protocol_section.get("designModule", {})
        phase = design_module.get("phases")
        if isinstance(phase, list) and phase:
            for phase_value in phase:
                if isinstance(phase_value, str) and phase_value.strip():
                    categories.add((phase_value.strip(), "phase"))

        # Extract study type
        study_type = design_module.get("studyType")
        if isinstance(study_type, str) and study_type.strip():
            categories.add((study_type.strip(), "study_type"))

        # Extract intervention types
        arms_interventions_module = protocol_section.get(
            "armsInterventionsModule", {}
        )
        interventions = arms_interventions_module.get("interventions", [])
        if isinstance(interventions, list):
            for intervention in interventions:
                if isinstance(intervention, dict):
                    intervention_type = intervention.get("type")
                    if isinstance(intervention_type, str) and intervention_type.strip():
                        categories.add(
                            (intervention_type.strip(), "intervention_type")
                        )

        # Extract organization/sponsor type
        sponsor_module = protocol_section.get("sponsorCollaboratorsModule", {})
        lead_sponsor = sponsor_module.get("leadSponsor", {})
        sponsor_class = lead_sponsor.get("class")
        if isinstance(sponsor_class, str) and sponsor_class.strip():
            categories.add((sponsor_class.strip(), "sponsor_type"))

        return categories

    def _extract_categories_from_fda(
        self, scraping_result: ScrapingResultDTO
    ) -> Set[tuple[str, str]]:
        """Extract categories from FDA drug label data.

        Args:
            scraping_result: Scraping result with FDA data

        Returns:
            Set of tuples (category_value, category_type)
        """
        categories: Set[tuple[str, str]] = set()

        if not scraping_result.data:
            return categories

        data = scraping_result.data

        # Extract route of administration if available
        route = data.get("route") or data.get("route_of_administration")
        if isinstance(route, str) and route.strip():
            categories.add((route.strip(), "route"))

        # Extract drug category/class if available
        drug_class = data.get("drug_class") or data.get("category")
        if isinstance(drug_class, str) and drug_class.strip():
            categories.add((drug_class.strip(), "drug_class"))

        # Note: FDA data structure may vary by API endpoint
        # This is a basic extraction that can be extended

        return categories

