"""Daily scheduler for scraper service."""

import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from typing import Callable, Awaitable

from shared.config import settings
from shared.logging.logger_interface import LoggerInterface
from shared.constants import ScheduleCron


class DailyScheduler:
    """Scheduler for running scraper tasks on a daily schedule."""

    def __init__(
        self,
        task: Callable[[], Awaitable[None]],
        logger: LoggerInterface,
    ) -> None:
        """Initialize daily scheduler.

        Args:
            task: Async function to execute on schedule
            logger: Logger instance
        """
        self._task = task
        self._logger = logger
        self._scheduler = AsyncIOScheduler()
        self._cron_expression = settings.scraper_schedule_cron

    async def start(self) -> None:
        """Start the scheduler."""
        await self._logger.info(
            f"Starting daily scheduler with cron: {self._cron_expression}"
        )

        # Parse cron expression (format: "minute hour day month weekday")
        parts = self._cron_expression.split()
        if len(parts) != 5:
            await self._logger.warning(
                f"Invalid cron expression: {self._cron_expression}, using default"
            )
            parts = ScheduleCron.DAILY_SCRAPER.split()

        minute, hour, day, month, weekday = parts

        trigger = CronTrigger(
            minute=minute,
            hour=hour,
            day=day,
            month=month,
            day_of_week=weekday,
        )

        self._scheduler.add_job(
            self._execute_task,
            trigger=trigger,
            id="daily_scraper",
            name="Daily Scraper Task",
        )

        self._scheduler.start()
        await self._logger.info("Daily scheduler started")

    async def stop(self) -> None:
        """Stop the scheduler."""
        await self._logger.info("Stopping daily scheduler")
        self._scheduler.shutdown(wait=True)
        await self._logger.info("Daily scheduler stopped")

    async def trigger_now(self) -> None:
        """Manually trigger the task immediately.

        Useful for testing or manual execution.
        """
        await self._logger.info("Manual trigger requested")
        await self._execute_task()

    async def _execute_task(self) -> None:
        """Execute the scheduled task with error handling."""
        try:
            await self._logger.info(
                f"Executing scheduled scraper task at {datetime.utcnow().isoformat()}"
            )
            await self._task()
            await self._logger.info("Scheduled scraper task completed successfully")
        except Exception as e:
            await self._logger.error(
                f"Scheduled scraper task failed: {str(e)}",
                extra={"error": str(e)},
            )
            # Don't re-raise - scheduler should continue running

