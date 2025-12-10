"""Factory pattern base implementation."""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Dict, Type, Any, Optional

T = TypeVar("T")


class Factory(ABC, Generic[T]):
    """Abstract factory base class for creating objects.

    Usage:
        class ScraperFactory(Factory[Scraper]):
            @staticmethod
            def create(key: str) -> Scraper:
                # Implementation
    """

    @staticmethod
    @abstractmethod
    def create(*args: Any, **kwargs: Any) -> T:
        """Create an instance of type T.

        Args:
            *args: Positional arguments for object creation
            **kwargs: Keyword arguments for object creation

        Returns:
            Instance of type T

        Raises:
            ValueError: If creation parameters are invalid
        """
        pass


class RegistryFactory(Factory[T]):
    """Factory implementation using a registry pattern.

    Allows registration of implementations by key.
    """

    def __init__(self) -> None:
        """Initialize registry factory."""
        self._registry: Dict[str, Type[T]] = {}

    def register(self, key: str, implementation: Type[T]) -> None:
        """Register an implementation for a key.

        Args:
            key: Key to register the implementation under
            implementation: Class to instantiate when key is requested
        """
        self._registry[key] = implementation

    def create(self, key: str, *args: Any, **kwargs: Any) -> T:
        """Create an instance using registered implementation.

        Args:
            key: Key to look up implementation
            *args: Positional arguments for object creation
            **kwargs: Keyword arguments for object creation

        Returns:
            Instance of registered type

        Raises:
            ValueError: If key is not registered
        """
        if key not in self._registry:
            raise ValueError(f"No implementation registered for key: {key}")

        implementation = self._registry[key]
        return implementation(*args, **kwargs)

    def get_registered_keys(self) -> list[str]:
        """Get all registered keys.

        Returns:
            List of registered keys
        """
        return list(self._registry.keys())

