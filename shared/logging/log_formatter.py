"""Log formatter for structured logging."""

import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from shared.types.common_types import JsonDict


class StructuredFormatter(logging.Formatter):
    """JSON structured log formatter."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON.

        Args:
            record: The log record to format

        Returns:
            JSON formatted log string
        """
        log_data: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "service": getattr(record, "service_name", "unknown"),
            "message": record.getMessage(),
        }

        # Add correlation ID if present
        correlation_id = getattr(record, "correlation_id", None)
        if correlation_id:
            log_data["correlation_id"] = correlation_id

        # Add extra fields
        extra = getattr(record, "extra_data", {})
        if extra:
            log_data["extra"] = extra

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


class PlainFormatter(logging.Formatter):
    """Plain text log formatter for development."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as plain text.

        Args:
            record: The log record to format

        Returns:
            Plain text formatted log string
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        service = getattr(record, "service_name", "unknown")
        correlation_id = getattr(record, "correlation_id", "")
        corr_str = f" [corr_id={correlation_id}]" if correlation_id else ""

        message = record.getMessage()
        level = record.levelname

        formatted = f"{timestamp} [{level}] [{service}]{corr_str} {message}"

        if record.exc_info:
            formatted += f"\n{self.formatException(record.exc_info)}"

        return formatted

