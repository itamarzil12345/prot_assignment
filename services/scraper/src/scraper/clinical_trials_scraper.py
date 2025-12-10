"""Clinical Trials scraper implementation."""

import uuid
from datetime import datetime, timezone
from typing import List
import httpx

from services.scraper.src.scraper.scraper_interface import ScraperInterface
from services.scraper.src.models.scraping_result_dto import ScrapingResultDTO
from services.scraper.src.errors.scraper_errors import ClinicalTrialsScrapingError
from shared.config import settings
from shared.constants import Timeouts
from shared.logging.logger_interface import LoggerInterface
from shared.types.enums import SourceType


class ClinicalTrialsScraper(ScraperInterface):
    """Scraper for ClinicalTrials.gov using their REST API v2."""

    def __init__(self, logger: LoggerInterface) -> None:
        """Initialize Clinical Trials scraper.

        Args:
            logger: Logger instance for logging operations
        """
        self._logger = logger
        self._base_url = settings.clinical_trials_api_base_url
        self._timeout = settings.clinical_trials_api_timeout_seconds

    async def get_source_name(self) -> str:
        """Get the name of the data source."""
        return "ClinicalTrials.gov"

    async def scrape(self) -> List[ScrapingResultDTO]:
        """Scrape ClinicalTrials.gov studies.

        Returns:
            List of scraped clinical trial results

        Raises:
            ClinicalTrialsScrapingError: If scraping fails
        """
        await self._logger.info("Starting ClinicalTrials.gov scraping")

        try:
            results: List[ScrapingResultDTO] = []

            # ClinicalTrials.gov API v2 endpoint for studies
            # Example: /studies?format=json&pageSize=100
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                url = f"{self._base_url}/studies"
                params = {"format": "json", "pageSize": 100}

                await self._logger.debug(f"Fetching from URL: {url}")

                response = await client.get(url, params=params)
                response.raise_for_status()

                data = response.json()

                # Process studies
                studies = data.get("studies", [])
                for study in studies:
                    try:
                        result = await self._process_study(study)
                        if result:
                            results.append(result)
                    except Exception as e:
                        await self._logger.warning(
                            f"Failed to process study: {str(e)}",
                            extra={"study_id": study.get("protocolSection", {}).get("identificationModule", {}).get("nctId")},
                        )
                        continue

            await self._logger.info(
                f"Clinical Trials scraping completed. Scraped {len(results)} studies"
            )
            return results

        except httpx.HTTPStatusError as e:
            error_msg = f"HTTP error during Clinical Trials scraping: {e.response.status_code}"
            await self._logger.error(
                error_msg, extra={"status_code": e.response.status_code}
            )
            raise ClinicalTrialsScrapingError(
                message=error_msg,
                error_code="CLINICAL_TRIALS_HTTP_ERROR",
                details={"status_code": e.response.status_code},
            ) from e

        except httpx.TimeoutException as e:
            error_msg = "Timeout during Clinical Trials scraping"
            await self._logger.error(error_msg)
            raise ClinicalTrialsScrapingError(
                message=error_msg,
                error_code="CLINICAL_TRIALS_TIMEOUT_ERROR",
            ) from e

        except Exception as e:
            error_msg = f"Unexpected error during Clinical Trials scraping: {str(e)}"
            await self._logger.error(error_msg)
            raise ClinicalTrialsScrapingError(
                message=error_msg,
                error_code="CLINICAL_TRIALS_UNEXPECTED_ERROR",
                details={"error": str(e)},
            ) from e

    async def _process_study(self, study: dict) -> ScrapingResultDTO | None:
        """Process a single clinical trial study.

        Args:
            study: Study dictionary from API

        Returns:
            ScrapingResultDTO if successful, None otherwise
        """
        try:
            protocol_section = study.get("protocolSection", {})
            identification = protocol_section.get("identificationModule", {})

            # Extract required fields
            nct_id = identification.get("nctId") or ""
            if not nct_id:
                return None

            brief_title = identification.get("briefTitle") or "Unknown Study"
            official_title = identification.get("officialTitle") or brief_title

            # Construct link
            link = f"https://clinicaltrials.gov/study/{nct_id}"

            result = ScrapingResultDTO(
                id=uuid.uuid4(),
                source_type=SourceType.CLINICAL_TRIALS,
                external_id=nct_id,
                title=official_title,
                data=study,
                link=link,
                scraped_at=datetime.now(timezone.utc),
            )

            return result

        except Exception as e:
            await self._logger.warning(
                f"Error processing study: {str(e)}",
                extra={"study": study.get("protocolSection", {}).get("identificationModule", {}).get("nctId")},
            )
            return None

