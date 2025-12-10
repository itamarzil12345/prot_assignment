"""Pydantic schemas for analysis result API requests and responses."""

from datetime import datetime
from uuid import UUID
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

from shared.types.enums import AnalysisType


class AnalysisResultResponse(BaseModel):
    """Response schema for analysis result."""

    id: UUID
    scraping_result_id: UUID
    analysis_type: AnalysisType
    keyword: Optional[str] = Field(None, max_length=255)
    frequency: int = Field(..., ge=0)
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "scraping_result_id": "223e4567-e89b-12d3-a456-426614174000",
                "analysis_type": "KEYWORD_FREQUENCY",
                "keyword": "treatment",
                "frequency": 10,
                "metadata": {"key": "value"},
                "created_at": "2024-01-01T00:00:00Z",
            }
        }


class AnalysisResultListResponse(BaseModel):
    """Response schema for list of analysis results."""

    items: list[AnalysisResultResponse]
    total: int
    limit: int
    offset: int


class AnalysisResultUpdateRequest(BaseModel):
    """Request schema for updating analysis result."""

    frequency: Optional[int] = Field(None, ge=0)
    metadata: Optional[Dict[str, Any]] = None


class AnalysisResultQueryParams(BaseModel):
    """Query parameters for listing analysis results."""

    limit: int = Field(default=50, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
    analysis_type: Optional[AnalysisType] = None
    scraping_result_id: Optional[UUID] = None

