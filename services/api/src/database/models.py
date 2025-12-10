"""SQLAlchemy ORM models."""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID
from typing import Any, Dict

from services.api.src.database.base import Base
from shared.constants import Tables
from shared.types.enums import SourceType, AnalysisType


class ScrapingResultModel(Base):
    """ORM model for scraping_results table."""

    __tablename__ = Tables.SCRAPING_RESULTS

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_type = Column(Enum(SourceType), nullable=False, index=True)
    external_id = Column(String(255), nullable=False, unique=True, index=True)
    title = Column(String(500), nullable=False)
    data = Column(JSON, nullable=False)
    link = Column(String(1000), nullable=False)
    scraped_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary.

        Returns:
            Dictionary representation of the model
        """
        return {
            "id": str(self.id),
            "source_type": self.source_type.value,
            "external_id": self.external_id,
            "title": self.title,
            "data": self.data,
            "link": self.link,
            "scraped_at": self.scraped_at.isoformat() if self.scraped_at else None,
        }


class AnalysisResultModel(Base):
    """ORM model for analysis_results table."""

    __tablename__ = Tables.ANALYSIS_RESULTS

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scraping_result_id = Column(
        UUID(as_uuid=True),
        ForeignKey(f"{Tables.SCRAPING_RESULTS}.id"),
        nullable=False,
        index=True,
    )
    analysis_type = Column(Enum(AnalysisType), nullable=False, index=True)
    keyword = Column(String(255), nullable=True, index=True)
    frequency = Column(Integer, nullable=False, default=0)
    meta_data = Column("metadata", JSON, nullable=True)  # Column named 'metadata' in DB, but 'meta_data' in Python (metadata is reserved)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary.

        Returns:
            Dictionary representation of the model
        """
        return {
            "id": str(self.id),
            "scraping_result_id": str(self.scraping_result_id),
            "analysis_type": self.analysis_type.value,
            "keyword": self.keyword,
            "frequency": self.frequency,
            "metadata": self.meta_data,  # Expose as 'metadata' in API
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

