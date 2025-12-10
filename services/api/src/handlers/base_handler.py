"""Base handler class for common handler functionality."""

from sqlalchemy.ext.asyncio import AsyncSession


class BaseHandler:
    """Base class for API handlers."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize base handler.

        Args:
            session: Database session
        """
        self._session = session

