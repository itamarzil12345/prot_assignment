"""Logger factory using Factory pattern."""

import logging
from typing import Optional

from shared.config import settings
from shared.constants import LogFiles
from shared.logging.log_formatter import PlainFormatter, StructuredFormatter
from shared.logging.log_handlers import FileLogHandlerFactory
from shared.logging.logger_interface import LoggerInterface
from shared.logging.service_logger import ServiceLogger
from shared.types.enums import LogLevel


class LoggerFactory:
    """Factory for creating logger instances."""

    @staticmethod
    def create_logger(service_name: str) -> LoggerInterface:
        """Create a configured logger instance for a service.

        Args:
            service_name: Name of the service

        Returns:
            Configured ServiceLogger instance
        """
        logger = logging.getLogger(service_name)
        logger.setLevel(getattr(logging, settings.log_level.value, logging.INFO))
        logger.handlers.clear()

        # Determine formatter based on environment
        use_json = settings.log_format.lower() == "json"
        formatter = (
            StructuredFormatter() if use_json else PlainFormatter()
        )

        # Create handlers for each log file
        # Logs go into service-specific directory: services/<service_name>/logs/
        service_log_dir = f"services/{service_name}/logs"
        handler_factory = FileLogHandlerFactory()

        # Error log handler
        error_handler = handler_factory.create_handler(
            log_file=LogFiles.ERROR,
            log_directory=service_log_dir,
            service_name=service_name,
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        logger.addHandler(error_handler)

        # Info log handler
        info_handler = handler_factory.create_handler(
            log_file=LogFiles.INFO,
            log_directory=service_log_dir,
            service_name=service_name,
        )
        info_handler.setLevel(logging.INFO)
        info_handler.setFormatter(formatter)
        logger.addHandler(info_handler)

        # Debug log handler
        debug_handler = handler_factory.create_handler(
            log_file=LogFiles.DEBUG,
            log_directory=service_log_dir,
            service_name=service_name,
        )
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.setFormatter(formatter)
        logger.addHandler(debug_handler)

        # Warning log handler
        warning_handler = handler_factory.create_handler(
            log_file=LogFiles.WARNING,
            log_directory=service_log_dir,
            service_name=service_name,
        )
        warning_handler.setLevel(logging.WARNING)
        warning_handler.setFormatter(formatter)
        logger.addHandler(warning_handler)

        # Audit log handler (custom level for audit trail)
        audit_handler = handler_factory.create_handler(
            log_file=LogFiles.AUDIT,
            log_directory=service_log_dir,
            service_name=service_name,
        )
        audit_handler.setLevel(logging.INFO)  # Use INFO level for audit
        audit_handler.setFormatter(formatter)
        logger.addHandler(audit_handler)

        return ServiceLogger(logger=logger, service_name=service_name)

