"""Analysis-specific error classes."""

from shared.errors import BaseApplicationError


class AnalysisError(BaseApplicationError):
    """Error raised when analysis fails."""

    def __init__(
        self,
        message: str,
        error_code: str = "ANALYSIS_ERROR",
        details: dict | None = None,
    ) -> None:
        """Initialize analysis error.

        Args:
            message: Error message
            error_code: Error code
            details: Optional additional details
        """
        super().__init__(message, error_code, details)


class KeywordAnalysisError(AnalysisError):
    """Error raised when keyword analysis fails."""

    def __init__(
        self,
        message: str,
        error_code: str = "KEYWORD_ANALYSIS_ERROR",
        details: dict | None = None,
    ) -> None:
        """Initialize keyword analysis error."""
        super().__init__(message, error_code, details)


class FrequencyAnalysisError(AnalysisError):
    """Error raised when frequency analysis fails."""

    def __init__(
        self,
        message: str,
        error_code: str = "FREQUENCY_ANALYSIS_ERROR",
        details: dict | None = None,
    ) -> None:
        """Initialize frequency analysis error."""
        super().__init__(message, error_code, details)

