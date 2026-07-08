"""
In-memory market data store.
"""

from __future__ import annotations

from collections import defaultdict, deque
from threading import RLock

from src.models.candle import Candle
from src.services.base_service import BaseService


class MarketData(BaseService):
    """
    Thread-safe in-memory candle storage.

    Stores a rolling window of candles for each symbol.
    """

    def __init__(self) -> None:
        super().__init__()

        self._lock = RLock()

        self._candles: dict[str, deque[Candle]] = defaultdict(
            lambda: deque(maxlen=self.settings.max_candles)
        )

        self.logger.info(
            "MarketData initialized (max_candles=%d)",
            self.settings.max_candles,
        )

    def add_candle(self, symbol: str, candle: Candle) -> None:
        """
        Add a candle for a symbol.
        """

        symbol = symbol.upper()

        with self._lock:
            self._candles[symbol].append(candle)

    def get_candles(self, symbol: str) -> list[Candle]:
        """
        Return all candles for a symbol.
        """

        symbol = symbol.upper()

        with self._lock:
            return list(self._candles.get(symbol, []))

    def get_latest_candle(self, symbol: str) -> Candle | None:
        """
        Return the latest candle.
        """

        symbol = symbol.upper()

        with self._lock:

            candles = self._candles.get(symbol)

            if not candles:
                return None

            return candles[-1]

    def get_previous_candle(self, symbol: str) -> Candle | None:
        """
        Return the previous candle.
        """

        symbol = symbol.upper()

        with self._lock:

            candles = self._candles.get(symbol)

            if candles is None or len(candles) < 2:
                return None

            return candles[-2]

    def get_candle_count(self, symbol: str) -> int:
        """
        Return number of candles stored.
        """

        symbol = symbol.upper()

        with self._lock:
            return len(self._candles.get(symbol, []))

    def has_symbol(self, symbol: str) -> bool:
        """
        Check whether a symbol exists.
        """

        symbol = symbol.upper()

        with self._lock:
            return symbol in self._candles

    def get_symbols(self) -> list[str]:
        """
        Return all loaded symbols.
        """

        with self._lock:
            return sorted(self._candles.keys())

    def remove_symbol(self, symbol: str) -> None:
        """
        Remove all candles for a symbol.
        """

        symbol = symbol.upper()

        with self._lock:

            self._candles.pop(symbol, None)

            self.logger.info(
                "Removed symbol %s from MarketData.",
                symbol,
            )

    def clear(self) -> None:
        """
        Remove all stored market data.
        """

        with self._lock:

            self._candles.clear()

            self.logger.info("MarketData cleared.")

    def symbol_count(self) -> int:
        """
        Return number of loaded symbols.
        """

        with self._lock:
            return len(self._candles)

    def is_empty(self) -> bool:
        """
        Return True if no data exists.
        """

        return self.symbol_count() == 0

    def add_candles(
            self,
            symbol: str,
            candles: list[Candle],
    ) -> None:

        symbol = symbol.upper()

        with self._lock:
            self._candles[symbol].extend(candles)

    def replace_latest_candle(
            self,
            symbol: str,
            candle: Candle,
    ) -> None:
        """
        Replace the latest candle.

        Used when historical data already contains the
        current minute and the WebSocket continues updating
        that candle.
        """

        symbol = symbol.upper()

        with self._lock:

            candles = self._candles[symbol]

            if candles:

                candles[-1] = candle

            else:

                candles.append(candle)