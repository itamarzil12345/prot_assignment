"""API routes."""

from services.api.src.routes.scraping_routes import router as scraping_router
from services.api.src.routes.analysis_routes import router as analysis_router

__all__ = ["scraping_router", "analysis_router"]

