"""Analysis strategy using Strategy pattern."""

from typing import List
from shared.patterns.strategy import Strategy, Context

from services.analysis.src.models.analysis_result_dto import AnalysisResultDTO
from services.scraper.src.models.scraping_result_dto import ScrapingResultDTO


class AnalysisStrategy(Strategy[ScrapingResultDTO, List[AnalysisResultDTO]]):
    """Strategy interface for analysis algorithms."""

    pass


class AnalysisContext(Context[ScrapingResultDTO, List[AnalysisResultDTO]]):
    """Context for executing analysis strategies."""

    pass

