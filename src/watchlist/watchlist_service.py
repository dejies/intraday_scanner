from __future__ import annotations

from typing import Optional
from dhanhq import MarketFeed

from src.watchlist.watchlist_snapshot import WatchlistSnapshot


class WatchlistService:
    """
    Monitors watchlist.csv and calculates
    added / removed symbols.
    """

    def __init__(
            self,
            universe_provider,
            instrument_master_service,
    ):
        self.universe_provider = universe_provider
        self.instrument_master_service = instrument_master_service

        self._instrument_by_security_id = {}
        self._symbols = set()

    def get_subscription_tuples(
            self,
            symbols: set[str],
    ) -> list[tuple]:

        subscriptions = []

        for symbol in sorted(symbols):

            instrument = self.instrument_master_service.get_by_symbol(symbol)

            if instrument is None:
                self.logger.warning(
                    "Unknown symbol in watchlist: %s",
                    symbol,
                )
                continue

            subscriptions.append(
                (
                    self._map_exchange(instrument.exchange),
                    str(instrument.security_id),
                    MarketFeed.Full,
                )
            )

        return subscriptions

    def subscribe_symbols(
            self,
            subscriptions: list[tuple],
    ):
        """
        Subscribe newly added instruments.
        """

        if not subscriptions:
            return

        self.logger.info(
            "Subscribing %d instruments.",
            len(subscriptions),
        )

        self.feed.subscribe_symbols(subscriptions)

    def unsubscribe_symbols(
            self,
            subscriptions: list[tuple],
    ):
        """
        Remove instruments from live feed.
        """

        if not subscriptions:
            return

        self.logger.info(
            "Unsubscribing %d instruments.",
            len(subscriptions),
        )

        self.feed.unsubscribe_symbols(subscriptions)

    @property
    def symbols(self) -> set[str]:
        return set(self._symbols)

    def load(self) -> WatchlistSnapshot:

        current = set(
            self.universe_provider.get_symbols()
        )

        self._symbols = current

        self._instrument_by_security_id.clear()

        for instrument in self.get_all():
            self._instrument_by_security_id[
                instrument.security_id
            ] = instrument

        return WatchlistSnapshot(
            symbols=current,
            added=current,
            removed=set(),
        )

    def refresh(
            self,
    ) -> WatchlistSnapshot:

        current = set(
            self.universe_provider.get_symbols()
        )

        added = current - self._symbols

        removed = self._symbols - current

        self._symbols = current

        self._instrument_by_security_id.clear()

        for instrument in self.get_all():
            self._instrument_by_security_id[
                instrument.security_id
            ] = instrument

        return WatchlistSnapshot(
            symbols=current,
            added=added,
            removed=removed,
        )



    def _map_exchange(self, exchange: str) -> int:

        value = self._EXCHANGE_MAP.get(exchange.upper())

        if value is None:
            raise ValueError(
                f"Unsupported exchange: {exchange}"
            )

        return value

    def get_all(self) -> list:
        instruments = []

        for symbol in sorted(self._symbols):
            instrument = self.instrument_master_service.get_by_symbol(symbol)

            if instrument is not None:
                instruments.append(instrument)

        return instruments

    def get_instrument_by_security_id(self, security_id):
        return self._instrument_by_security_id.get(security_id)