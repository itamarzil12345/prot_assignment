"""Error handling middleware for FastAPI."""

from typing import Callable
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from shared.errors import (
    BaseApplicationError,
    DatabaseError,
    NotFoundError,
    ValidationError,
)
from services.api.src.errors.api_errors import (
    APIError,
    APINotFoundError,
    APIValidationError,
)
from shared.constants import ErrorMessages


class ErrorHandlerMiddleware:
    """Middleware for handling and mapping errors."""

    @staticmethod
    async def handle_error(request: Request, exc: Exception) -> JSONResponse:
        """Handle exceptions and return appropriate error response.

        Args:
            request: FastAPI request object
            exc: Exception that was raised

        Returns:
            JSONResponse with error details
        """
        if isinstance(exc, APINotFoundError):
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "error": {
                        "message": exc.message,
                        "error_code": exc.error_code,
                        "details": exc.details,
                    }
                },
            )

        if isinstance(exc, APIValidationError):
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "error": {
                        "message": exc.message,
                        "error_code": exc.error_code,
                        "details": exc.details,
                    }
                },
            )

        if isinstance(exc, APIError):
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "error": {
                        "message": exc.message,
                        "error_code": exc.error_code,
                        "details": exc.details,
                    }
                },
            )

        if isinstance(exc, NotFoundError):
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "error": {
                        "message": exc.message,
                        "error_code": exc.error_code,
                        "details": exc.details,
                    }
                },
            )

        if isinstance(exc, ValidationError):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error": {
                        "message": exc.message,
                        "error_code": exc.error_code,
                        "details": exc.details,
                    }
                },
            )

        if isinstance(exc, DatabaseError):
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": {
                        "message": ErrorMessages.INTERNAL_SERVER_ERROR,
                        "error_code": exc.error_code,
                        "details": {},
                    }
                },
            )

        if isinstance(exc, RequestValidationError):
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={
                    "error": {
                        "message": ErrorMessages.VALIDATION_ERROR,
                        "error_code": "VALIDATION_ERROR",
                        "details": {"validation_errors": exc.errors()},
                    }
                },
            )

        if isinstance(exc, HTTPException):
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "error": {
                        "message": exc.detail,
                        "error_code": f"HTTP_{exc.status_code}",
                        "details": {},
                    }
                },
            )

        # Generic error handler
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "message": ErrorMessages.INTERNAL_SERVER_ERROR,
                    "error_code": "INTERNAL_SERVER_ERROR",
                    "details": {},
                }
            },
        )

