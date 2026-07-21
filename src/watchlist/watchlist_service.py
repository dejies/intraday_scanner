from __future__ import annotations

from pathlib import Path
from typing import Optional
from dhanhq import MarketFeed
import pandas as pd

from src.watchlist.watchlist_snapshot import WatchlistSnapshot


class WatchlistService:
    """
    Monitors watchlist.csv and calculates
    added / removed symbols.
    """

    def __init__(
            self,
            csv_path: str,
            instrument_master_service,
    ):
        self.csv_path = Path(csv_path)
        self.instrument_master_service = instrument_master_service
        self._instrument_by_security_id = {}
        self._symbols = set()
        self._last_modified = 0.0

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

        current = self._read_symbols()

        snapshot = WatchlistSnapshot(
            symbols=current,
            added=current,
            removed=set(),
        )

        self._symbols = current

        self._instrument_by_security_id = {}

        for instrument in self.get_all():
            self._instrument_by_security_id[instrument.security_id] = instrument

        self._last_modified = self.csv_path.stat().st_mtime

        return snapshot

    def refresh(self) -> Optional[WatchlistSnapshot]:

        modified = self.csv_path.stat().st_mtime

        if modified == self._last_modified:
            return None

        current = self._read_symbols()

        added = current - self._symbols

        removed = self._symbols - current

        self._symbols = current

        self._instrument_by_security_id = {}

        for instrument in self.get_all():
            self._instrument_by_security_id[instrument.security_id] = instrument

        self._last_modified = modified

        return WatchlistSnapshot(
            symbols=current,
            added=added,
            removed=removed,
        )

    def _read_symbols(self) -> set[str]:

        df = pd.read_csv(self.csv_path)

        return {
            str(symbol).strip().upper()
            for symbol in df["symbol"]
            if str(symbol).strip()
        }

    _EXCHANGE_MAP = {
        "IDX": 0,
        "NSE": 1,
        "NSE_FNO": 2,
        "NSE_CURR": 3,
        "BSE": 4,
        "MCX": 5,
        "BSE_CURR": 7,
        "BSE_FNO": 8,
    }

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