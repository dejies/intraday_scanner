from __future__ import annotations

from abc import ABC, abstractmethod


class SymbolProvider(ABC):
    """
    Supplies the current set of symbols.
    """

    @abstractmethod
    def get_symbols(self) -> set[str]:
        """
        Return the current symbol universe.
        """
        raise NotImplementedError