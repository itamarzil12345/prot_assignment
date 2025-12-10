"""Main entry point for analysis service."""

import asyncio
import signal
from datetime import timezone
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from services.analysis.src.config import ANALYSIS_ENABLED, ANALYSIS_BATCH_SIZE
from services.analysis.src.constants import SERVICE_NAME
from services.analysis.src.scheduler.analysis_scheduler import AnalysisScheduler
from services.analysis.src.analyzer.keyword_analyzer import KeywordAnalyzer
from services.analysis.src.analyzer.condition_grouping_analyzer import (
    ConditionGroupingAnalyzer,
)
from services.analysis.src.repository.analysis_repository import AnalysisRepository
from services.analysis.src.repository.analysis_repository_interface import (
    AnalysisResultDTO,
)
from services.scraper.src.repository.scraping_repository import ScrapingRepository
from shared.config import settings
from shared.database.engine_factory import create_database_engine
from shared.logging.logger_factory import LoggerFactory
from shared.logging.logger_interface import LoggerInterface
from shared.types.enums import AnalysisType


class AnalysisService:
    """Main analysis service orchestrator."""

    def __init__(self) -> None:
        """Initialize analysis service."""
        self._logger: LoggerInterface = LoggerFactory.create_logger(SERVICE_NAME)
        self._scheduler: AnalysisScheduler | None = None
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

    async def run_analysis_task(self) -> None:
        """Execute the analysis task for all analysis types."""
        await self._logger.info("Starting analysis task")

        analysis_types = [
            AnalysisType.KEYWORD_FREQUENCY,
            AnalysisType.CONDITION_GROUPING,
        ]

        for analysis_type in analysis_types:
            try:
                await self._analyze_unprocessed(analysis_type)
            except Exception as e:
                await self._logger.error(
                    f"Failed to analyze with {analysis_type.value}: {str(e)}",
                    extra={"analysis_type": analysis_type.value, "error": str(e)},
                )
                # Continue with next analysis type even if one fails

        await self._logger.info("Analysis task completed")

    async def _analyze_unprocessed(self, analysis_type: AnalysisType) -> None:
        """Analyze unprocessed scraping results for a specific analysis type.

        Args:
            analysis_type: Type of analysis to perform
        """
        await self._logger.info(f"Starting {analysis_type.value} analysis")

        async with self._session_factory() as session:
            analysis_repo = AnalysisRepository(session)
            scraping_repo = ScrapingRepository(session)

            # Get unprocessed scraping result IDs
            unprocessed_ids = await analysis_repo.get_unprocessed_scraping_ids(
                limit=ANALYSIS_BATCH_SIZE, analysis_type=analysis_type
            )

            if not unprocessed_ids:
                await self._logger.info(f"No unprocessed results for {analysis_type.value}")
                return

            await self._logger.info(
                f"Found {len(unprocessed_ids)} unprocessed results for {analysis_type.value}"
            )

            # Get analyzer based on analysis type
            analyzer = self._get_analyzer(analysis_type)

            analyzed_count = 0
            error_count = 0

            for scraping_id in unprocessed_ids:
                try:
                    # Get scraping result
                    scraping_result = await scraping_repo.get_by_id(scraping_id)

                    if not scraping_result:
                        await self._logger.warning(
                            f"Scraping result not found: {scraping_id}"
                        )
                        continue

                    # Convert repository DTO to model DTO
                    from services.scraper.src.models.scraping_result_dto import (
                        ScrapingResultDTO as ModelScrapingResultDTO,
                    )

                    model_result = ModelScrapingResultDTO(
                        id=scraping_result.id,
                        source_type=scraping_result.source_type,
                        external_id=scraping_result.external_id,
                        title=scraping_result.title,
                        data=scraping_result.data,
                        link=scraping_result.link,
                        scraped_at=scraping_result.scraped_at,
                    )

                    # Perform analysis
                    analysis_results = await analyzer.analyze(model_result)

                    # Save analysis results
                    if analysis_results:
                        repo_results = [
                            AnalysisResultDTO(
                                id=result.id,
                                scraping_result_id=result.scraping_result_id,
                                analysis_type=result.analysis_type,
                                keyword=result.keyword,
                                frequency=result.frequency,
                                metadata=result.metadata,
                                created_at=result.created_at,
                            )
                            for result in analysis_results
                        ]

                        await analysis_repo.create_batch(repo_results)
                        analyzed_count += 1

                except Exception as e:
                    error_count += 1
                    await self._logger.error(
                        f"Failed to analyze scraping result {scraping_id}: {str(e)}",
                        extra={"scraping_id": str(scraping_id), "error": str(e)},
                    )
                    continue

            await session.commit()

            await self._logger.info(
                f"Completed {analysis_type.value} analysis: "
                f"{analyzed_count} analyzed, {error_count} errors"
            )

    def _get_analyzer(self, analysis_type: AnalysisType):
        """Get analyzer instance for analysis type.

        Args:
            analysis_type: Type of analysis

        Returns:
            Analyzer instance
        """
        if analysis_type == AnalysisType.KEYWORD_FREQUENCY:
            return KeywordAnalyzer(self._logger)

        if analysis_type == AnalysisType.CONDITION_GROUPING:
            return ConditionGroupingAnalyzer(self._logger)

        raise ValueError(f"Unknown analysis type: {analysis_type}")

    async def start(self) -> None:
        """Start the analysis service."""
        if not ANALYSIS_ENABLED:
            await self._logger.warning("Analysis service is disabled")
            return

        await self._logger.info("Starting analysis service")

        self._running = True

        # Create and start scheduler
        self._scheduler = AnalysisScheduler(self.run_analysis_task, self._logger)

        # Start scheduler (runs in background)
        asyncio.create_task(self._scheduler.start())

        # Keep service running
        try:
            while self._running:
                await asyncio.sleep(60)
        except KeyboardInterrupt:
            await self._logger.info("Received shutdown signal")

    async def stop(self) -> None:
        """Stop the analysis service."""
        await self._logger.info("Stopping analysis service")
        self._running = False

        if self._scheduler:
            await self._scheduler.stop()

        await self._engine.dispose()
        await self._logger.info("Analysis service stopped")


async def main() -> None:
    """Main entry point."""
    service = AnalysisService()

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

