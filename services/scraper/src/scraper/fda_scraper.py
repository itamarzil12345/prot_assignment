"""FDA DailyMed scraper implementation."""

import uuid
from datetime import datetime, timezone
from typing import List
import httpx

from services.scraper.src.scraper.scraper_interface import ScraperInterface
from services.scraper.src.models.scraping_result_dto import ScrapingResultDTO
from services.scraper.src.errors.scraper_errors import FDAScrapingError
from shared.config import settings
from shared.constants import Timeouts
from shared.logging.logger_interface import LoggerInterface
from shared.types.enums import SourceType


class FDAScraper(ScraperInterface):
    """Scraper for FDA DailyMed drug labels."""

    def __init__(self, logger: LoggerInterface) -> None:
        """Initialize FDA scraper.

        Args:
            logger: Logger instance for logging operations
        """
        self._logger = logger
        self._base_url = settings.dailymed_base_url
        self._timeout = Timeouts.HTTP_API

    async def get_source_name(self) -> str:
        """Get the name of the data source."""
        return "FDA DailyMed"

    async def scrape(self) -> List[ScrapingResultDTO]:
        """Scrape FDA DailyMed drug labels.

        Returns:
            List of scraped drug label results

        Raises:
            FDAScrapingError: If scraping fails
        """
        await self._logger.info("Starting FDA DailyMed scraping")

        try:
            results: List[ScrapingResultDTO] = []

            # DailyMed uses a REST API-like structure
            # Example: https://dailymed.nlm.nih.gov/dailymed/services/v2/drugnames.json
            # We'll scrape from the drug names endpoint
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                url = f"{self._base_url}/dailymed/services/v2/drugnames.json"
                
                await self._logger.debug(f"Fetching from URL: {url}")
                
                response = await client.get(url)
                response.raise_for_status()

                data = response.json()

                # Process the drug names
                if "data" in data and isinstance(data["data"], list):
                    for item in data["data"]:
                        try:
                            result = await self._process_drug_item(item)
                            if result:
                                results.append(result)
                        except Exception as e:
                            await self._logger.warning(
                                f"Failed to process drug item: {str(e)}",
                                extra={"item": item},
                            )
                            continue

            await self._logger.info(
                f"FDA scraping completed. Scraped {len(results)} items"
            )
            return results

        except httpx.HTTPStatusError as e:
            error_msg = f"HTTP error during FDA scraping: {e.response.status_code}"
            await self._logger.error(error_msg, extra={"status_code": e.response.status_code})
            raise FDAScrapingError(
                message=error_msg,
                error_code="FDA_HTTP_ERROR",
                details={"status_code": e.response.status_code},
            ) from e

        except httpx.TimeoutException as e:
            error_msg = "Timeout during FDA scraping"
            await self._logger.error(error_msg)
            raise FDAScrapingError(
                message=error_msg,
                error_code="FDA_TIMEOUT_ERROR",
            ) from e

        except Exception as e:
            error_msg = f"Unexpected error during FDA scraping: {str(e)}"
            await self._logger.error(error_msg)
            raise FDAScrapingError(
                message=error_msg,
                error_code="FDA_UNEXPECTED_ERROR",
                details={"error": str(e)},
            ) from e

    async def _process_drug_item(self, item: dict) -> ScrapingResultDTO | None:
        """Process a single drug item from the API response.

        Args:
            item: Drug item dictionary from API

        Returns:
            ScrapingResultDTO if successful, None otherwise
        """
        try:
            # Extract required fields
            external_id = item.get("drug_name_id") or item.get("id") or str(uuid.uuid4())
            title = item.get("drug_name") or item.get("name") or "Unknown Drug"
            
            # Construct link
            drug_name_id = item.get("drug_name_id") or item.get("id", "")
            link = f"{self._base_url}/dailymed/drugInfo.cfm?setid={drug_name_id}" if drug_name_id else self._base_url

            result = ScrapingResultDTO(
                id=uuid.uuid4(),
                source_type=SourceType.FDA_DRUG_LABELS,
                external_id=str(external_id),
                title=str(title),
                data=item,
                link=link,
                scraped_at=datetime.now(timezone.utc),
            )

            return result

        except Exception as e:
            await self._logger.warning(
                f"Error processing drug item: {str(e)}",
                extra={"item": item},
            )
            return None

