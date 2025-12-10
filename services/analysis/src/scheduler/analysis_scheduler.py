"""Scheduler for analysis service."""

import asyncio
from datetime import datetime
from typing import Callable, Awaitable

from shared.config import settings
from shared.logging.logger_interface import LoggerInterface


class AnalysisScheduler:
    """Scheduler for running analysis tasks periodically."""

    def __init__(
        self,
        task: Callable[[], Awaitable[None]],
        logger: LoggerInterface,
    ) -> None:
        """Initialize analysis scheduler.

        Args:
            task: Async function to execute on schedule
            logger: Logger instance
        """
        self._task = task
        self._logger = logger
        self._interval_seconds = settings.analysis_poll_interval_seconds
        self._running = False

    async def start(self) -> None:
        """Start the scheduler."""
        await self._logger.info(
            f"Starting analysis scheduler with interval: {self._interval_seconds}s"
        )

        self._running = True

        # Run initial analysis
        await self._execute_task()

        # Start periodic execution
        while self._running:
            await asyncio.sleep(self._interval_seconds)
            if self._running:
                await self._execute_task()

    async def stop(self) -> None:
        """Stop the scheduler."""
        await self._logger.info("Stopping analysis scheduler")
        self._running = False

    async def trigger_now(self) -> None:
        """Manually trigger the task immediately."""
        await self._logger.info("Manual trigger requested")
        await self._execute_task()

    async def _execute_task(self) -> None:
        """Execute the scheduled task with error handling."""
        try:
            await self._logger.info(
                f"Executing scheduled analysis task at {datetime.utcnow().isoformat()}"
            )
            await self._task()
            await self._logger.info("Scheduled analysis task completed successfully")
        except Exception as e:
            await self._logger.error(
                f"Scheduled analysis task failed: {str(e)}",
                extra={"error": str(e)},
            )
            # Don't re-raise - scheduler should continue running

