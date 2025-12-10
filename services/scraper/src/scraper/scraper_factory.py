"""Factory for creating scraper instances."""

from shared.patterns.factory import Factory
from services.scraper.src.scraper.scraper_interface import ScraperInterface
from services.scraper.src.scraper.fda_scraper import FDAScraper
from services.scraper.src.scraper.clinical_trials_scraper import ClinicalTrialsScraper
from shared.logging.logger_interface import LoggerInterface
from shared.types.enums import SourceType


class ScraperFactory(Factory[ScraperInterface]):
    """Factory for creating scraper instances based on source type."""

    @staticmethod
    def create(source_type: SourceType, logger: LoggerInterface) -> ScraperInterface:
        """Create a scraper instance for the given source type.

        Args:
            source_type: Type of data source to scrape
            logger: Logger instance for the scraper

        Returns:
            ScraperInterface instance

        Raises:
            ValueError: If source type is unknown
        """
        if source_type == SourceType.FDA_DRUG_LABELS:
            return FDAScraper(logger=logger)

        if source_type == SourceType.CLINICAL_TRIALS:
            return ClinicalTrialsScraper(logger=logger)

        raise ValueError(f"Unknown source type: {source_type}")

