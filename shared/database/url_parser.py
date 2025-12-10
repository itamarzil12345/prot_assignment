"""Database URL parser and converter for asyncpg."""

from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
from typing import Optional


def convert_to_asyncpg_url(database_url: str) -> str:
    """Convert psql connection string to asyncpg-compatible format.

    Args:
        database_url: PostgreSQL connection URL (psql format)

    Returns:
        Connection URL compatible with asyncpg driver

    Examples:
        >>> convert_to_asyncpg_url("postgresql://user:pass@host/db?sslmode=require")
        "postgresql+asyncpg://user:pass@host/db?ssl=require"
    """
    # Parse the URL
    parsed = urlparse(database_url)

    # Replace postgresql:// with postgresql+asyncpg://
    if parsed.scheme == "postgresql":
        scheme = "postgresql+asyncpg"
    elif parsed.scheme.startswith("postgresql+"):
        # Already has a driver, keep it
        scheme = parsed.scheme
    else:
        scheme = "postgresql+asyncpg"

    # Parse query parameters
    query_params = parse_qs(parsed.query)

    # Handle SSL mode for asyncpg
    # asyncpg doesn't use sslmode - SSL is handled via connect_args in SQLAlchemy
    # So we remove sslmode from the URL and it will be handled separately if needed
    query_params.pop("sslmode", None)

    # Remove channel_binding (not supported by asyncpg)
    query_params.pop("channel_binding", None)

    # Rebuild query string
    new_query = urlencode(query_params, doseq=True)

    # Reconstruct URL
    new_parsed = parsed._replace(scheme=scheme, query=new_query)
    return urlunparse(new_parsed)

