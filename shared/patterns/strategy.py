"""Strategy pattern base implementation."""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Any

TInput = TypeVar("TInput")
TOutput = TypeVar("TOutput")


class Strategy(ABC, Generic[TInput, TOutput]):
    """Abstract strategy interface for interchangeable algorithms.

    Usage:
        class AnalysisStrategy(Strategy[Data, Result]):
            @abstractmethod
            async def execute(self, data: Data) -> Result:
                pass
    """

    @abstractmethod
    async def execute(self, input_data: TInput) -> TOutput:
        """Execute the strategy algorithm.

        Args:
            input_data: Input data for the strategy

        Returns:
            Result of strategy execution

        Raises:
            StrategyError: If strategy execution fails
        """
        pass


class Context(Generic[TInput, TOutput]):
    """Context class that uses a strategy.

    Allows switching strategies at runtime.
    """

    def __init__(self, strategy: Strategy[TInput, TOutput]) -> None:
        """Initialize context with a strategy.

        Args:
            strategy: Strategy to use for execution
        """
        self._strategy = strategy

    def set_strategy(self, strategy: Strategy[TInput, TOutput]) -> None:
        """Set a new strategy.

        Args:
            strategy: New strategy to use
        """
        self._strategy = strategy

    async def execute(self, input_data: TInput) -> TOutput:
        """Execute the current strategy.

        Args:
            input_data: Input data for the strategy

        Returns:
            Result of strategy execution
        """
        return await self._strategy.execute(input_data)

