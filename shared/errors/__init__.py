"""Shared error classes and error handling utilities."""

from shared.errors.base_errors import (
    BaseApplicationError,
    DatabaseError,
    ValidationError,
    NotFoundError,
    ExternalServiceError,
)

__all__ = [
    "BaseApplicationError",
    "DatabaseError",
    "ValidationError",
    "NotFoundError",
    "ExternalServiceError",
]

