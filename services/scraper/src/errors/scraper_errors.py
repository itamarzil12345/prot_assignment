"""Scraper-specific error classes."""

from shared.errors import ExternalServiceError


class ScrapingError(ExternalServiceError):
    """Error raised when scraping fails."""

    def __init__(
        self,
        message: str,
        service_name: str,
        error_code: str = "SCRAPING_ERROR",
        details: dict | None = None,
    ) -> None:
        """Initialize scraping error.

        Args:
            message: Error message
            service_name: Name of the scraping service
            error_code: Error code
            details: Optional additional details
        """
        super().__init__(message, error_code, service_name, details)


class FDAScrapingError(ScrapingError):
    """Error raised when FDA scraping fails."""

    def __init__(
        self, message: str, error_code: str = "FDA_SCRAPING_ERROR", details: dict | None = None
    ) -> None:
        """Initialize FDA scraping error."""
        super().__init__(message, "FDA_DailyMed", error_code, details)


class ClinicalTrialsScrapingError(ScrapingError):
    """Error raised when Clinical Trials scraping fails."""

    def __init__(
        self,
        message: str,
        error_code: str = "CLINICAL_TRIALS_SCRAPING_ERROR",
        details: dict | None = None,
    ) -> None:
        """Initialize Clinical Trials scraping error."""
        super().__init__(message, "ClinicalTrials.gov", error_code, details)

