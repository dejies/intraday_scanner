"""
Scanner Engine

Runs all enabled scanners and collects trading signals.
"""

from __future__ import annotations

from src.scanners.breakout import BreakoutScanner
from src.scanners.trend import TrendScanner
from src.scanners.volume import VolumeScanner
from src.services.market_data import MarketData
from src.core.market_data_store import MarketDataStore
from src.services.watchlist import WatchlistService
from src.models.signal import Signal
from src.models.enums import SignalType
from src.services.opening_range_service import OpeningRangeService
from src.strategies import (
    StrategyManager,
    EMAAlignmentStrategy,
    RSIStrategy,
    MACDStrategy,
    ORBStrategy
)
class Scanner:
    """
    Executes all enabled scanners.
    """

    def __init__(
        self,
        market_data: MarketData,
        market_store: MarketDataStore,
        watchlist: WatchlistService,
        opening_range_service: OpeningRangeService,
    ) -> None:

        self.market_data = market_data
        self.market_store = market_store
        self.watchlist = watchlist
        self._opening_range_service = opening_range_service
        self._strategy_manager = StrategyManager()
        self._strategy_manager.register(
            EMAAlignmentStrategy()
        )
        self._strategy_manager.register(
            RSIStrategy()
        )
        self._strategy_manager.register(
            MACDStrategy()
        )
        self._strategy_manager.register(
            ORBStrategy(
                opening_range_service=self._opening_range_service,
            )
        )

    # ------------------------------------------------------------------

    def scan(self):
        """
        Run all scanners and return trading signals.
        """

        signals: dict[int, Signal] = {}

        for stock in self.market_store.get_all_stocks():

            strategy_results = self._strategy_manager.evaluate(
                stock
            )

            for result in strategy_results:

                signal = Signal(
                    security_id=stock.instrument.security_id,
                    strategy=result.strategy,
                    signal_type=(
                        SignalType.BUY
                        if result.signal == "BUY"
                        else SignalType.SELL
                    ),
                    signal_price=float(stock.tick.ltp),
                    current_ltp=float(stock.tick.ltp),
                    confidence=result.confidence,
                    message=result.reason,
                    timestamp=stock.tick.timestamp,
                )

                existing = signals.get(
                    stock.instrument.security_id
                )

                if (
                        existing is None
                        or signal.confidence > existing.confidence
                ):
                    signals[
                        stock.instrument.security_id
                    ] = signal

        for signal in signals.values():
            self.market_store.update_signal(signal)

        return list(signals.values())

    @property
    def strategy_manager(self) -> StrategyManager:
        return self._strategy_manager