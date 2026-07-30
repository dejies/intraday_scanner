from __future__ import annotations

from src.database import SQLiteManager
from src.database.universe_repository import UniverseRepository

from src.services.universe.models import (
    MarketUniverse,
    UniverseStock,
)
from src.services.universe.providers.base_provider import (
    MarketUniverseProvider,
)


class UniverseSyncService:
    """
    Downloads the latest market universe from all configured providers,
    resolves Dhan instrument IDs, and atomically updates the SQLite cache.
    """

    def __init__(
        self,
        sqlite: SQLiteManager,
        repository: UniverseRepository,
        providers: list[MarketUniverseProvider],
        instrument_master_service,
    ):
        self._sqlite = sqlite
        self._repository = repository
        self._providers = providers
        self._instrument_master = instrument_master_service

    # ---------------------------------------------------------

    def sync(self) -> int:

        universe = MarketUniverse()

        #
        # Merge all provider results
        #
        for provider in self._providers:

            provider_universe = provider.load()

            for stock in provider_universe.stocks.values():
                universe.add_stock(stock)

            for membership in provider_universe.memberships:
                universe.add_membership(membership)

        #
        # Resolve Dhan instrument IDs
        #
        resolved_stocks = []

        for stock in universe.stocks.values():

            instrument = self._instrument_master.get_by_symbol(
                stock.symbol
            )

            if instrument is None:
                continue

            resolved_stocks.append(
                UniverseStock(
                    symbol=stock.symbol,
                    company_name=stock.company_name,
                    security_id=str(instrument.security_id),
                    exchange=instrument.exchange,
                    segment=instrument.segment,
                )
            )

        #
        # Atomic database update
        #
        self._sqlite.begin()

        try:

            self._repository.delete_all()

            self._repository.save_stocks(
                resolved_stocks
            )

            self._repository.save_memberships(
                list(universe.memberships)
            )

            # Future enhancement:
            # self._repository.update_last_sync()

            self._sqlite.commit()

        except Exception:

            self._sqlite.rollback()
            raise

        return len(resolved_stocks)