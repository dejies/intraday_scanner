"""
Thread-safe runtime market data store.

The MarketDataStore is the single source of truth for all live market data.
Every module (WebSocket, Scanner, Dashboard, Alerts) interacts with this
store instead of communicating directly with each other.
"""

from __future__ import annotations
from collections.abc import Callable
from threading import RLock
from typing import Iterable

from src.models.enums import SignalType
from src.models.market_status import MarketStatus
from src.models.stock_state import StockState
from src.models.instrument import Instrument
from datetime import datetime
from src.models.tick import Tick
from src.models.candle import Candle
from src.models.indicator import IndicatorData
from src.models.signal import Signal


class MarketDataStore:
    """
    Thread-safe runtime storage for the scanner.
    """

    def __init__(self) -> None:
        self._stocks: dict[int, StockState] = {}
        self._market_status = MarketStatus()
        self._lock = RLock()


    def register_instrument(self, instrument: Instrument) -> None:
        """
        Register an instrument for runtime tracking.

        A StockState is created for every registered instrument.
        If the instrument already exists, it is ignored.
        """
        with self._lock:
            if instrument.security_id in self._stocks:
                return

            self._stocks[instrument.security_id] = StockState(
                instrument=instrument
            )

    def register_instruments(
            self,
            instruments: Iterable[Instrument]
    ) -> None:
        """
        Register multiple instruments.
        """
        with self._lock:
            for instrument in instruments:
                self.register_instrument(instrument)

            self._market_status.watching_count = len(self._stocks)

    def get_stock(self, security_id: int) -> StockState | None:
        """
        Returns the runtime state for a stock.
        """
        with self._lock:
            return self._stocks.get(security_id)

    def get_all_stocks(self) -> tuple[StockState, ...]:
        """
        Returns all registered stocks.

        A tuple is returned instead of the internal dictionary to prevent
        accidental modification by callers.
        """
        with self._lock:
            return tuple(self._stocks.values())

    def get_instruments(self) -> tuple[Instrument, ...]:
        """
        Returns all registered instruments.
        """
        with self._lock:
            return tuple(
                stock.instrument
                for stock in self._stocks.values()
            )

    def contains(self, security_id: int) -> bool:
        """
        Returns True if the instrument is registered.
        """
        with self._lock:
            return security_id in self._stocks

    def stock_count(self) -> int:
        """
        Returns the number of registered instruments.
        """
        with self._lock:
            return len(self._stocks)

    def update_tick(
            self,
            tick: Tick,
    ) -> None:
        """
        Updates the latest market tick.
        """
        with self._lock:
            stock = self._get_required_stock(
                tick.security_id
            )

            stock.tick = tick

            self._touch(stock)

            self._market_status.last_tick_at = stock.last_updated

    def get_tick(
            self,
            security_id: int,
    ) -> Tick | None:
        """
        Returns the latest market tick.
        """
        with self._lock:
            stock = self._get_optional_stock(
                security_id
            )

            return None if stock is None else stock.tick

    def update_candle(
            self,
            security_id: int,
            candle: Candle,
    ) -> None:
        """
        Updates the latest candle.
        """
        with self._lock:
            stock = self._get_required_stock(
                security_id
            )

            stock.current_candle = candle

            self._touch(stock)

    def get_candle(
            self,
            security_id: int,
    ) -> Candle | None:
        """
        Returns the current candle.
        """
        with self._lock:
            stock = self._get_optional_stock(
                security_id
            )

            return None if stock is None else stock.current_candle

    def _get_required_stock(
            self,
            security_id: int,
    ) -> StockState:
        """
        Returns the StockState for the given instrument.

        Raises:
            KeyError: If the instrument is not registered.
        """
        stock = self._stocks.get(security_id)

        if stock is None:
            raise KeyError(
                f"Instrument not registered: {security_id}"
            )

        return stock

    def _touch(
            self,
            stock: StockState,
    ) -> None:
        """
        Updates the runtime timestamp for a stock.
        """
        stock.last_updated = datetime.now()


    def update_indicator(
            self,
            security_id: int,
            indicator: IndicatorData,
    ) -> None:
        """
        Updates the latest calculated indicators.
        """
        with self._lock:
            stock = self._get_required_stock(
                security_id
            )

            stock.indicator = indicator

            self._touch(stock)

    def get_indicator(
            self,
            security_id: int,
    ) -> IndicatorData | None:
        """
        Returns the latest indicator values.
        """
        with self._lock:
            stock = self._get_optional_stock(
                security_id
            )

            return None if stock is None else stock.indicator

    def _get_optional_stock(
            self,
            security_id: int,
    ) -> StockState | None:
        """
        Returns the StockState for the given instrument.

        Returns:
            StockState if registered, otherwise None.
        """
        return self._stocks.get(security_id)

    def get_signal(
            self,
            security_id: int,
    ) -> Signal | None:
        """
        Returns the active signal.
        """
        with self._lock:
            stock = self._get_optional_stock(
                security_id
            )

            return None if stock is None else stock.active_signal


    # ------------------------------------------------------------------
    # Dashboard Query APIs
    # ------------------------------------------------------------------

    from collections.abc import Callable

    def _filter_stocks(
            self,
            predicate: Callable[[StockState], bool],
    ) -> tuple[StockState, ...]:
        """
        Returns all stocks matching the given predicate.

        This is the common filtering method used by dashboard queries.
        """
        with self._lock:
            return tuple(
                stock
                for stock in self._stocks.values()
                if predicate(stock)
            )

    def get_enabled_stocks(self) -> tuple[StockState, ...]:
        """
        Returns all enabled stocks.
        """
        return self._filter_stocks(
            lambda stock: stock.enabled
        )

    def get_buy_signals(self) -> tuple[StockState, ...]:
        """
        Returns all active BUY signals.
        """
        return self._filter_stocks(
            lambda stock: (
                    stock.active_signal is not None
                    and stock.active_signal.is_active
                    and stock.active_signal.signal_type == SignalType.BUY
            )
        )

    def get_sell_signals(self) -> tuple[StockState, ...]:
        """
        Returns all active SELL signals.
        """
        return self._filter_stocks(
            lambda stock: (
                    stock.active_signal is not None
                    and stock.active_signal.is_active
                    and stock.active_signal.signal_type == SignalType.SELL
            )
        )

    def get_active_signals(self) -> tuple[StockState, ...]:
        """
        Returns all active BUY and SELL signals.
        """
        return self._filter_stocks(
            lambda stock: (
                    stock.active_signal is not None
                    and stock.active_signal.is_active
            )
        )

    def buy_count(self) -> int:
        """
        Returns the number of active BUY signals.
        """
        return len(self.get_buy_signals())

    def sell_count(self) -> int:
        """
        Returns the number of active SELL signals.
        """
        return len(self.get_sell_signals())

    # ------------------------------------------------------------------
    # Market Status
    # ------------------------------------------------------------------

    def get_market_status(self) -> MarketStatus:
        """
        Returns the application runtime status.
        """
        with self._lock:
            return self._market_status

    def update_market_status(
            self,
            updater,
    ) -> None:
        """
        Updates the application runtime status.
        """

        with self._lock:
            updater(self._market_status)

    # ------------------------------------------------------------------
    # Utility APIs
    # ------------------------------------------------------------------

    def clear_runtime_data(self) -> None:
        """
        Clears runtime market data while preserving registered instruments.
        """
        with self._lock:
            for stock in self._stocks.values():
                stock.tick = None
                stock.current_candle = None
                stock.indicator = None
                stock.active_signal = None

    def clear(self) -> None:
        """
        Clears the entire MarketDataStore.
        """
        with self._lock:
            self._stocks.clear()
            self._market_status = MarketStatus()

    # ------------------------------------------------------------------
    # Python Helper Methods
    # ------------------------------------------------------------------

    def __len__(self) -> int:
        return self.stock_count()

    def __contains__(self, security_id: int) -> bool:
        return self.contains(security_id)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"stocks={self.stock_count()}, "
            f"buy={self.buy_count()}, "
            f"sell={self.sell_count()})"
        )

    def update_signal(
            self,
            signal: Signal,
    ) -> None:
        """
        Updates the active signal for a stock.

        If an active signal already exists, it is replaced.
        """
        with self._lock:
            stock = self._get_required_stock(
                signal.security_id
            )

            stock.active_signal = signal

            self._touch(stock)

    def has_active_signal(
            self,
            security_id: int,
    ) -> bool:
        """
        Returns True if the stock has an active signal.
        """
        with self._lock:
            stock = self._get_optional_stock(security_id)
            return (
                    stock is not None
                    and stock.active_signal is not None
                    and stock.active_signal.is_active
            )

    def clear_signal(
            self,
            security_id: int,
    ) -> None:
        """
        Clears the active signal for a stock.
        """
        with self._lock:
            stock = self._get_required_stock(security_id)

            if stock.active_signal is None:
                return

            stock.active_signal = None

            self._touch(stock)
