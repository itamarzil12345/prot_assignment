"""Logger interface for dependency inversion."""

from abc import ABC, abstractmethod
from typing import Optional

from shared.types.common_types import JsonDict


class LoggerInterface(ABC):
    """Abstract interface for logging functionality."""

    @abstractmethod
    async def error(
        self,
        message: str,
        correlation_id: Optional[str] = None,
        extra: Optional[JsonDict] = None,
    ) -> None:
        """Log an error message.

        Args:
            message: The error message to log
            correlation_id: Optional correlation ID for request tracking
            extra: Optional additional context as dictionary
        """
        pass

    @abstractmethod
    async def info(
        self,
        message: str,
        correlation_id: Optional[str] = None,
        extra: Optional[JsonDict] = None,
    ) -> None:
        """Log an info message.

        Args:
            message: The info message to log
            correlation_id: Optional correlation ID for request tracking
            extra: Optional additional context as dictionary
        """
        pass

    @abstractmethod
    async def debug(
        self,
        message: str,
        correlation_id: Optional[str] = None,
        extra: Optional[JsonDict] = None,
    ) -> None:
        """Log a debug message.

        Args:
            message: The debug message to log
            correlation_id: Optional correlation ID for request tracking
            extra: Optional additional context as dictionary
        """
        pass

    @abstractmethod
    async def warning(
        self,
        message: str,
        correlation_id: Optional[str] = None,
        extra: Optional[JsonDict] = None,
    ) -> None:
        """Log a warning message.

        Args:
            message: The warning message to log
            correlation_id: Optional correlation ID for request tracking
            extra: Optional additional context as dictionary
        """
        pass

    @abstractmethod
    async def audit(
        self,
        message: str,
        correlation_id: Optional[str] = None,
        extra: Optional[JsonDict] = None,
    ) -> None:
        """Log an audit message.

        Args:
            message: The audit message to log
            correlation_id: Optional correlation ID for request tracking
            extra: Optional additional context as dictionary
        """
        pass

