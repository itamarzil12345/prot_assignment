"""Base error classes for the application."""

from typing import Optional


class BaseApplicationError(Exception):
    """Base exception class for all application errors."""

    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[dict] = None,
    ) -> None:
        """Initialize base application error.

        Args:
            message: Error message
            error_code: Optional error code for categorization
            details: Optional additional error details
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}


class DatabaseError(BaseApplicationError):
    """Error raised for database operations."""

    def __init__(
        self,
        message: str,
        error_code: str = "DATABASE_ERROR",
        details: Optional[dict] = None,
    ) -> None:
        """Initialize database error."""
        super().__init__(message, error_code, details)


class ValidationError(BaseApplicationError):
    """Error raised for validation failures."""

    def __init__(
        self,
        message: str,
        error_code: str = "VALIDATION_ERROR",
        details: Optional[dict] = None,
    ) -> None:
        """Initialize validation error."""
        super().__init__(message, error_code, details)


class NotFoundError(BaseApplicationError):
    """Error raised when a resource is not found."""

    def __init__(
        self,
        message: str,
        error_code: str = "NOT_FOUND",
        details: Optional[dict] = None,
    ) -> None:
        """Initialize not found error."""
        super().__init__(message, error_code, details)


class ExternalServiceError(BaseApplicationError):
    """Error raised for external service failures."""

    def __init__(
        self,
        message: str,
        error_code: str = "EXTERNAL_SERVICE_ERROR",
        service_name: Optional[str] = None,
        details: Optional[dict] = None,
    ) -> None:
        """Initialize external service error.

        Args:
            message: Error message
            error_code: Error code
            service_name: Name of the external service
            details: Optional additional details
        """
        super().__init__(message, error_code, details)
        self.service_name = service_name

