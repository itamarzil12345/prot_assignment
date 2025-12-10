"""Factory for creating database engines with proper SSL configuration."""

from urllib.parse import urlparse, parse_qs
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from typing import Optional

from shared.config import settings
from shared.database.url_parser import convert_to_asyncpg_url


def create_database_engine(
    pool_size: int,
    max_overflow: int,
    pool_timeout: int,
    pool_recycle: int,
) -> AsyncEngine:
    """Create async database engine with proper SSL configuration.

    Args:
        pool_size: Connection pool size
        max_overflow: Maximum overflow connections
        pool_timeout: Pool timeout in seconds
        pool_recycle: Pool recycle time in seconds

    Returns:
        Configured async SQLAlchemy engine
    """
    # Convert URL for asyncpg
    asyncpg_url = convert_to_asyncpg_url(settings.database_url)

    # Check if SSL is required from original URL
    parsed_original = urlparse(settings.database_url)
    query_params = parse_qs(parsed_original.query)
    ssl_required = query_params.get("sslmode", ["disable"])[0] == "require"

    # Configure connect args for SSL
    connect_args = {}
    if ssl_required:
        connect_args["ssl"] = True

    engine = create_async_engine(
        asyncpg_url,
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_timeout=pool_timeout,
        pool_recycle=pool_recycle,
        connect_args=connect_args,
        echo=False,
    )

    return engine

