"""Pydantic schemas for scraping result API requests and responses."""

from datetime import datetime
from uuid import UUID
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator

from shared.types.enums import SourceType


class ScrapingResultResponse(BaseModel):
    """Response schema for scraping result."""

    id: UUID
    source_type: SourceType
    external_id: str = Field(..., min_length=1, max_length=255)
    title: str = Field(..., min_length=1, max_length=500)
    data: Dict[str, Any]
    link: str = Field(..., min_length=1, max_length=1000)
    scraped_at: datetime

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "source_type": "FDA_DRUG_LABELS",
                "external_id": "drug-123",
                "title": "Example Drug Label",
                "data": {"key": "value"},
                "link": "https://example.com/drug",
                "scraped_at": "2024-01-01T00:00:00Z",
            }
        }


class ScrapingResultListResponse(BaseModel):
    """Response schema for list of scraping results."""

    items: list[ScrapingResultResponse]
    total: int
    limit: int
    offset: int


class ScrapingResultUpdateRequest(BaseModel):
    """Request schema for updating scraping result."""

    title: Optional[str] = Field(None, min_length=1, max_length=500)
    data: Optional[Dict[str, Any]] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        """Validate title is not empty if provided."""
        if v is not None and not v.strip():
            raise ValueError("Title cannot be empty")
        return v


class ScrapingResultQueryParams(BaseModel):
    """Query parameters for listing scraping results."""

    limit: int = Field(default=50, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
    source_type: Optional[SourceType] = None

