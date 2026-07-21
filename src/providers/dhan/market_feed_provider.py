"""
Abstract Market Feed Provider.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class MarketFeedProvider(ABC):
    """
    Interface implemented by all market feed providers.
    """

    @abstractmethod
    def connect(self) -> None:
        """Prepare the provider."""

    @abstractmethod
    def start(self) -> None:
        """Start receiving market data."""

    @abstractmethod
    def stop(self) -> None:
        """Stop receiving market data."""

    @abstractmethod
    def is_connected(self) -> bool:
        """Return current connection state."""