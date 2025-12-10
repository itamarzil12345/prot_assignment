"""Service logger implementation."""

import logging
from typing import Optional

from shared.logging.logger_interface import LoggerInterface
from shared.types.common_types import JsonDict


class ServiceLogger(LoggerInterface):
    """Concrete implementation of LoggerInterface."""

    def __init__(self, logger: logging.Logger, service_name: str) -> None:
        """Initialize service logger.

        Args:
            logger: Python logging.Logger instance
            service_name: Name of the service
        """
        self._logger = logger
        self._service_name = service_name

    def _log(
        self,
        level: int,
        message: str,
        correlation_id: Optional[str] = None,
        extra: Optional[JsonDict] = None,
    ) -> None:
        """Internal logging method.

        Args:
            level: Logging level
            message: Log message
            correlation_id: Optional correlation ID
            extra: Optional extra data
        """
        log_extra = {
            "service_name": self._service_name,
        }

        if correlation_id:
            log_extra["correlation_id"] = correlation_id

        if extra:
            log_extra["extra_data"] = extra

        self._logger.log(level, message, extra=log_extra)

    async def error(
        self,
        message: str,
        correlation_id: Optional[str] = None,
        extra: Optional[JsonDict] = None,
    ) -> None:
        """Log an error message."""
        self._log(logging.ERROR, message, correlation_id, extra)

    async def info(
        self,
        message: str,
        correlation_id: Optional[str] = None,
        extra: Optional[JsonDict] = None,
    ) -> None:
        """Log an info message."""
        self._log(logging.INFO, message, correlation_id, extra)

    async def debug(
        self,
        message: str,
        correlation_id: Optional[str] = None,
        extra: Optional[JsonDict] = None,
    ) -> None:
        """Log a debug message."""
        self._log(logging.DEBUG, message, correlation_id, extra)

    async def warning(
        self,
        message: str,
        correlation_id: Optional[str] = None,
        extra: Optional[JsonDict] = None,
    ) -> None:
        """Log a warning message."""
        self._log(logging.WARNING, message, correlation_id, extra)

    async def audit(
        self,
        message: str,
        correlation_id: Optional[str] = None,
        extra: Optional[JsonDict] = None,
    ) -> None:
        """Log an audit message.

        Audit messages are written to the audit.log file.
        """
        # Audit uses INFO level but is handled by audit handler
        self._log(logging.INFO, f"[AUDIT] {message}", correlation_id, extra)

