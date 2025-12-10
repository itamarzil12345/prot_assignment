"""Adapter pattern implementation."""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic

TAdaptee = TypeVar("TAdaptee")
TTarget = TypeVar("TTarget")


class Adapter(ABC, Generic[TAdaptee, TTarget]):
    """Abstract adapter interface for adapting one interface to another.

    Usage:
        class ExternalAPIAdapter(Adapter[ExternalAPI, InternalAPI]):
            def adapt(self, external: ExternalAPI) -> InternalAPI:
                # Convert external format to internal format
    """

    @abstractmethod
    def adapt(self, adaptee: TAdaptee) -> TTarget:
        """Adapt adaptee to target format.

        Args:
            adaptee: Object to adapt

        Returns:
            Adapted object
        """
        pass

