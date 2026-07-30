from __future__ import annotations

from abc import ABC, abstractmethod


class UniverseProvider(ABC):
    """
    Provides the current market universe.
    """

    @abstractmethod
    def get_symbols(self) -> set[str]:
        """
        Return the current set of symbols.
        """
        raise NotImplementedError