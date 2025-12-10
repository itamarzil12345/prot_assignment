"""Main FastAPI application."""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from services.api.src.config import API_HOST, API_PORT
from services.api.src.constants import SERVICE_NAME
from services.api.src.database.base import init_db, close_db
from services.api.src.middleware.error_handler import ErrorHandlerMiddleware
from services.api.src.middleware.logging_middleware import LoggingMiddleware
from services.api.src.routes import scraping_router, analysis_router
from services.api.src.routes.health_routes import router as health_router
from shared.config import settings
from shared.logging.logger_factory import LoggerFactory


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown.

    Args:
        app: FastAPI application

    Yields:
        None
    """
    # Startup
    logger = LoggerFactory.create_logger(SERVICE_NAME)
    await logger.info("Starting API service")

    # Initialize database
    try:
        await init_db()
        await logger.info("Database initialized")
    except Exception as e:
        await logger.error(f"Failed to initialize database: {str(e)}", extra={"error": str(e)})
        raise

    yield

    # Shutdown
    await logger.info("Shutting down API service")
    await close_db()
    await logger.info("API service stopped")


# Create FastAPI app
app = FastAPI(
    title="Protego Health Backend API",
    description="API for accessing scraped FDA drug labels and clinical trials data",
    version=settings.app_version,
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add logging middleware
logger = LoggerFactory.create_logger(SERVICE_NAME)
app.add_middleware(LoggingMiddleware, logger=logger)

# Add error handlers
handler = ErrorHandlerMiddleware()
app.add_exception_handler(Exception, handler.handle_error)

# Include routers
app.include_router(health_router)
app.include_router(scraping_router)
app.include_router(analysis_router)


@app.get("/")
async def root() -> dict:
    """Root endpoint.

    Returns:
        API information
    """
    return {
        "service": "Protego Health Backend API",
        "version": settings.app_version,
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "services.api.src.main:app",
        host=API_HOST,
        port=API_PORT,
        reload=API_RELOAD,
    )

