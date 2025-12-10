"""Log handlers for file-based logging."""

import logging
import logging.handlers
from pathlib import Path
from typing import Optional

from shared.constants import LogFiles, Limits


class FileLogHandlerFactory:
    """Factory for creating file-based log handlers."""

    @staticmethod
    def create_handler(
        log_file: str,
        log_directory: str,
        service_name: str,
        max_bytes: int = Limits.LOG_MAX_BYTES,
        backup_count: int = Limits.LOG_BACKUP_COUNT,
    ) -> logging.handlers.RotatingFileHandler:
        """Create a rotating file handler.

        Args:
            log_file: Name of the log file
            log_directory: Base directory for logs
            service_name: Name of the service
            max_bytes: Maximum bytes per log file
            backup_count: Number of backup files to keep

        Returns:
            Configured RotatingFileHandler
        """
        # Log path is already service-specific from logger_factory
        log_path = Path(log_directory) / log_file
        log_path.parent.mkdir(parents=True, exist_ok=True)

        handler = logging.handlers.RotatingFileHandler(
            filename=str(log_path),
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )

        return handler

