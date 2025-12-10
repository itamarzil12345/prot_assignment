"""Pydantic schemas for analysis result API requests and responses."""

from datetime import datetime
from uuid import UUID
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict

from shared.types.enums import AnalysisType


class AnalysisResultResponse(BaseModel):
    """Response schema for analysis result."""

    id: UUID
    scraping_result_id: Optional[UUID] = Field(None, description="UUID of the scraping result. Null for global aggregations like FREQUENT_TERMS.")
    analysis_type: AnalysisType
    keyword: Optional[str] = Field(None, max_length=255, description="Keyword or phrase. Can be a single word or multi-word phrase like 'drug is safe to use'.")
    frequency: int = Field(..., ge=0)
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "summary": "KEYWORD_FREQUENCY example (single word)",
                    "value": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "scraping_result_id": "223e4567-e89b-12d3-a456-426614174000",
                        "analysis_type": "KEYWORD_FREQUENCY",
                        "keyword": "treatment",
                        "frequency": 10,
                        "metadata": {"source_type": "CLINICAL_TRIALS", "title": "Clinical Trial Study"},
                        "created_at": "2024-01-01T00:00:00Z",
                    }
                },
                {
                    "summary": "KEYWORD_FREQUENCY example (phrase)",
                    "value": {
                        "id": "123e4567-e89b-12d3-a456-426614174001",
                        "scraping_result_id": "223e4567-e89b-12d3-a456-426614174000",
                        "analysis_type": "KEYWORD_FREQUENCY",
                        "keyword": "drug is safe to use",
                        "frequency": 5,
                        "metadata": {"source_type": "FDA_DRUG_LABELS", "title": "Drug Safety Label"},
                        "created_at": "2024-01-01T00:00:00Z",
                    }
                },
                {
                    "summary": "FREQUENT_TERMS example (global aggregation)",
                    "value": {
                        "id": "123e4567-e89b-12d3-a456-426614174002",
                        "scraping_result_id": None,
                        "analysis_type": "FREQUENT_TERMS",
                        "keyword": "drug is safe to use",
                        "frequency": 150,
                        "metadata": {"document_count": 45, "rank": 1, "aggregated_from": "KEYWORD_FREQUENCY"},
                        "created_at": "2024-01-01T00:00:00Z",
                    }
                },
                {
                    "summary": "CONDITION_GROUPING example",
                    "value": {
                        "id": "123e4567-e89b-12d3-a456-426614174003",
                        "scraping_result_id": "223e4567-e89b-12d3-a456-426614174000",
                        "analysis_type": "CONDITION_GROUPING",
                        "keyword": "Diabetes Mellitus",
                        "frequency": 1,
                        "metadata": {"source_type": "CLINICAL_TRIALS", "grouped_by": "condition"},
                        "created_at": "2024-01-01T00:00:00Z",
                    }
                }
            ]
        }
    )


class AnalysisResultListResponse(BaseModel):
    """Response schema for list of analysis results."""

    items: list[AnalysisResultResponse]
    total: int
    limit: int
    offset: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "items": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "scraping_result_id": "223e4567-e89b-12d3-a456-426614174000",
                        "analysis_type": "KEYWORD_FREQUENCY",
                        "keyword": "drug is safe to use",
                        "frequency": 15,
                        "metadata": {"source_type": "FDA_DRUG_LABELS"},
                        "created_at": "2024-01-01T00:00:00Z",
                    },
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174001",
                        "scraping_result_id": "223e4567-e89b-12d3-a456-426614174000",
                        "analysis_type": "KEYWORD_FREQUENCY",
                        "keyword": "treatment",
                        "frequency": 10,
                        "metadata": {"source_type": "CLINICAL_TRIALS"},
                        "created_at": "2024-01-01T00:00:00Z",
                    }
                ],
                "total": 1250,
                "limit": 50,
                "offset": 0,
            }
        }
    )


class AnalysisResultUpdateRequest(BaseModel):
    """Request schema for updating analysis result."""

    frequency: Optional[int] = Field(None, ge=0, description="Updated frequency value")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Updated metadata dictionary")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "frequency": 25,
                "metadata": {
                    "source_type": "CLINICAL_TRIALS",
                    "title": "Updated Study Title",
                    "note": "Manually corrected frequency"
                }
            }
        }
    )


class AnalysisResultQueryParams(BaseModel):
    """Query parameters for listing analysis results."""

    limit: int = Field(default=50, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
    analysis_type: Optional[AnalysisType] = None
    scraping_result_id: Optional[UUID] = None
    keyword: Optional[str] = Field(None, max_length=255, description="Filter by keyword (case-insensitive partial match)")


class MostFrequentTermResponse(BaseModel):
    """Response schema for most frequent term."""

    keyword: str = Field(..., description="Keyword or phrase. Can be a single word or multi-word phrase like 'drug is safe to use'.")
    total_frequency: int = Field(..., ge=0, description="Total frequency across all documents")
    document_count: int = Field(..., ge=0, description="Number of documents containing this keyword")

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "summary": "Single word example",
                    "value": {
                        "keyword": "treatment",
                        "total_frequency": 1250,
                        "document_count": 45,
                    }
                },
                {
                    "summary": "Multi-word phrase example",
                    "value": {
                        "keyword": "drug is safe to use",
                        "total_frequency": 890,
                        "document_count": 32,
                    }
                }
            ]
        }
    )


class MostFrequentTermsResponse(BaseModel):
    """Response schema for list of most frequent terms."""

    items: list[MostFrequentTermResponse]
    limit: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "items": [
                    {
                        "keyword": "drug is safe to use",
                        "total_frequency": 890,
                        "document_count": 32,
                    },
                    {
                        "keyword": "participants",
                        "total_frequency": 750,
                        "document_count": 28,
                    },
                    {
                        "keyword": "clinical trials",
                        "total_frequency": 650,
                        "document_count": 45,
                    },
                    {
                        "keyword": "safety assessment",
                        "total_frequency": 540,
                        "document_count": 22,
                    },
                    {
                        "keyword": "treatment",
                        "total_frequency": 520,
                        "document_count": 38,
                    }
                ],
                "limit": 10,
            }
        }
    )

