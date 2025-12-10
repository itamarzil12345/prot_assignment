"""Logging middleware for FastAPI."""

import time
import uuid
from typing import Callable
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from shared.logging.logger_interface import LoggerInterface


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP requests and responses."""

    def __init__(self, app: Callable, logger: LoggerInterface) -> None:
        """Initialize logging middleware.

        Args:
            app: FastAPI application
            logger: Logger instance
        """
        super().__init__(app)
        self._logger = logger

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and log details.

        Args:
            request: FastAPI request
            call_next: Next middleware/handler

        Returns:
            Response object
        """
        # Generate correlation ID
        correlation_id = str(uuid.uuid4())

        # Log request
        start_time = time.time()
        await self._logger.audit(
            f"Request: {request.method} {request.url.path}",
            correlation_id=correlation_id,
            extra={
                "method": request.method,
                "path": request.url.path,
                "query_params": str(request.query_params),
                "client_host": request.client.host if request.client else None,
            },
        )

        # Add correlation ID to request state
        request.state.correlation_id = correlation_id

        # Process request
        try:
            response = await call_next(request)
            process_time = time.time() - start_time

            # Log response
            await self._logger.audit(
                f"Response: {request.method} {request.url.path} - {response.status_code}",
                correlation_id=correlation_id,
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "process_time": process_time,
                },
            )

            # Add correlation ID to response header
            response.headers["X-Correlation-ID"] = correlation_id

            return response

        except Exception as e:
            process_time = time.time() - start_time

            await self._logger.error(
                f"Request failed: {request.method} {request.url.path} - {str(e)}",
                correlation_id=correlation_id,
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "error": str(e),
                    "process_time": process_time,
                },
            )

            raise

