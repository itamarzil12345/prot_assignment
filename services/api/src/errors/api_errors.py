"""API-specific error classes."""

from typing import Optional
from shared.errors import BaseApplicationError, NotFoundError, ValidationError


class APIError(BaseApplicationError):
    """Base error for API operations."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: str = "API_ERROR",
        details: Optional[dict] = None,
    ) -> None:
        """Initialize API error.

        Args:
            message: Error message
            status_code: HTTP status code
            error_code: Error code
            details: Optional additional details
        """
        super().__init__(message, error_code, details)
        self.status_code = status_code


class APINotFoundError(NotFoundError, APIError):
    """Error raised when API resource is not found."""

    def __init__(
        self,
        message: str,
        error_code: str = "API_NOT_FOUND",
        details: Optional[dict] = None,
    ) -> None:
        """Initialize API not found error."""
        super().__init__(message, error_code, details)
        self.status_code = 404


class APIValidationError(ValidationError, APIError):
    """Error raised when API request validation fails."""

    def __init__(
        self,
        message: str,
        error_code: str = "API_VALIDATION_ERROR",
        details: Optional[dict] = None,
    ) -> None:
        """Initialize API validation error."""
        super().__init__(message, error_code, details)
        self.status_code = 400

