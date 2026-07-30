"""
Base interface for all market universe providers.

A provider supplies one or more market universes such as:

- NIFTY500
- NIFTY MIDCAP 150
- NIFTY SMALLCAP 250
- F&O (future)
- Sector Indices (future)

Providers know NOTHING about:

- SQLite
- Scanner
- Dashboard
- WebSocket
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from src.services.universe.models import MarketUniverse


class MarketUniverseProvider(ABC):
    """
    Base class for all universe providers.
    """

    @abstractmethod
    def load(self) -> MarketUniverse:
        """
        Load the complete market universe from this provider.

        Returns
        -------
        MarketUniverse
        """
        raise NotImplementedError