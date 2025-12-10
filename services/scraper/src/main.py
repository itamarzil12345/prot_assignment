"""Main entry point for scraper service."""

import asyncio
import signal
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from services.scraper.src.config import SCRAPER_ENABLED
from services.scraper.src.constants import SERVICE_NAME
from services.scraper.src.scheduler.daily_scheduler import DailyScheduler
from services.scraper.src.scraper.scraper_factory import ScraperFactory
from services.scraper.src.repository.scraping_repository import ScrapingRepository
from services.scraper.src.repository.scraping_repository_interface import (
    ScrapingResultDTO as RepoScrapingResultDTO,
)
from shared.config import settings
from shared.database.engine_factory import create_database_engine
from shared.logging.logger_factory import LoggerFactory
from shared.logging.logger_interface import LoggerInterface
from shared.types.enums import SourceType


class ScraperService:
    """Main scraper service orchestrator."""

    def __init__(self) -> None:
        """Initialize scraper service."""
        self._logger: LoggerInterface = LoggerFactory.create_logger(SERVICE_NAME)
        self._scheduler: DailyScheduler | None = None
        self._engine = create_database_engine(
            pool_size=settings.db_pool_size,
            max_overflow=settings.db_max_overflow,
            pool_timeout=settings.db_pool_timeout,
            pool_recycle=settings.db_pool_recycle,
        )
        self._session_factory = async_sessionmaker(
            self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        self._running = False

    async def run_scraping_task(self) -> None:
        """Execute the scraping task for all sources."""
        await self._logger.info("Starting scraping task")

        sources = [SourceType.FDA_DRUG_LABELS, SourceType.CLINICAL_TRIALS]

        for source_type in sources:
            try:
                await self._scrape_source(source_type)
            except Exception as e:
                await self._logger.error(
                    f"Failed to scrape {source_type.value}: {str(e)}",
                    extra={"source_type": source_type.value, "error": str(e)},
                )
                # Continue with next source even if one fails

        await self._logger.info("Scraping task completed")

    async def _scrape_source(self, source_type: SourceType) -> None:
        """Scrape data from a specific source.

        Args:
            source_type: Type of source to scrape
        """
        await self._logger.info(f"Scraping source: {source_type.value}")

        # Create scraper
        scraper = ScraperFactory.create(source_type, self._logger)

        # Scrape data
        results = await scraper.scrape()

        # Save to database
        async with self._session_factory() as session:
            repository = ScrapingRepository(session)

            saved_count = 0
            skipped_count = 0

            for result in results:
                try:
                    # Check if already exists
                    exists = await repository.exists_by_external_id(
                        result.external_id, result.source_type
                    )

                    if exists:
                        skipped_count += 1
                        await self._logger.debug(
                            f"Skipping duplicate: {result.external_id}"
                        )
                        continue

                    # Convert to repository DTO
                    repo_dto = RepoScrapingResultDTO(
                        id=result.id,
                        source_type=result.source_type,
                        external_id=result.external_id,
                        title=result.title,
                        data=result.data,
                        link=result.link,
                        scraped_at=result.scraped_at,
                    )

                    await repository.create(repo_dto)
                    saved_count += 1

                except Exception as e:
                    await self._logger.error(
                        f"Failed to save result {result.external_id}: {str(e)}",
                        extra={"external_id": result.external_id, "error": str(e)},
                    )
                    continue

            await session.commit()

        await self._logger.info(
            f"Completed scraping {source_type.value}: "
            f"{saved_count} saved, {skipped_count} skipped"
        )

    async def start(self) -> None:
        """Start the scraper service."""
        if not SCRAPER_ENABLED:
            await self._logger.warning("Scraper service is disabled")
            return

        await self._logger.info("Starting scraper service")

        self._running = True

        # Create and start scheduler
        self._scheduler = DailyScheduler(self.run_scraping_task, self._logger)
        await self._scheduler.start()

        # Run initial scraping
        await self.run_scraping_task()

        # Keep service running
        try:
            while self._running:
                await asyncio.sleep(60)  # Sleep and check running status
        except KeyboardInterrupt:
            await self._logger.info("Received shutdown signal")

    async def stop(self) -> None:
        """Stop the scraper service."""
        await self._logger.info("Stopping scraper service")
        self._running = False

        if self._scheduler:
            await self._scheduler.stop()

        await self._engine.dispose()
        await self._logger.info("Scraper service stopped")


async def main() -> None:
    """Main entry point."""
    service = ScraperService()

    # Handle shutdown signals
    def signal_handler(signum: int, frame: object) -> None:
        """Handle shutdown signal."""
        asyncio.create_task(service.stop())

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        await service.start()
    except Exception as e:
        await service._logger.error(f"Service failed: {str(e)}", extra={"error": str(e)})
        raise
    finally:
        await service.stop()


if __name__ == "__main__":
    asyncio.run(main())

