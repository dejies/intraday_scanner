from __future__ import annotations

from src.database.universe_repository import UniverseRepository

from src.services.universe.models import (
    MarketUniverse,
    UniverseMembership,
    UniverseStock,
)


class UniverseManager:
    """
    In-memory access layer for the market universe.

    Responsibilities
    ----------------
    - Load universe from repository
    - Cache universe
    - Fast symbol lookup

    Knows NOTHING about:

    - NSE
    - SQLite implementation
    - WebSocket
    - Scanner
    """

    def __init__(
        self,
        repository: UniverseRepository,
    ):
        self._repository = repository

        self._universe: MarketUniverse | None = None

    # ---------------------------------------------------------

    def load(self) -> MarketUniverse:

        if self._universe is None:
            self.refresh()

        return self._universe

    # ---------------------------------------------------------

    def refresh(self):

        self._universe = self._repository.load_universe()

    # ---------------------------------------------------------

    def stocks(
        self,
    ) -> list[UniverseStock]:

        return list(
            self.load().stocks.values()
        )

    # ---------------------------------------------------------

    def memberships(
        self,
    ) -> list[UniverseMembership]:

        return list(
            self.load().memberships
        )

    # ---------------------------------------------------------

    def symbols(
        self,
    ) -> set[str]:

        return self.load().symbols()

    # ---------------------------------------------------------

    def contains(
        self,
        symbol: str,
    ) -> bool:

        return self.load().contains(symbol)

    # ---------------------------------------------------------

    def get(
        self,
        symbol: str,
    ) -> UniverseStock | None:

        return self.load().get(symbol)

    # ---------------------------------------------------------

    def count(self) -> int:

        return len(
            self.load().stocks
        )

    # ---------------------------------------------------------

    def clear_cache(self):

        self._universe = None