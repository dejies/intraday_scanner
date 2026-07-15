"""
MACD trading strategy.
"""

from __future__ import annotations

from src.core.market_data_store import StockState
from src.strategies.base_strategy import BaseStrategy
from src.strategies.strategy_result import StrategyResult
from src.strategies.strategy_filters import StrategyFilters

class MACDStrategy(BaseStrategy):

    def __init__(self):

        super().__init__("MACD Momentum")

    # ---------------------------------------------------------

    def evaluate(
        self,
        stock: StockState,
    ) -> StrategyResult | None:

        indicator = stock.indicator
        tick = stock.tick

        if indicator is None or tick is None:
            return None

        if (
            indicator.macd is None
            or indicator.macd_signal is None
            or indicator.macd_histogram is None
        ):
            return None

        #
        # BUY
        #
        if (
                indicator.macd > indicator.macd_signal
                and indicator.macd_histogram > 0
                and indicator.macd > 0
                and StrategyFilters.adx_bullish(stock)
                and StrategyFilters.above_vwap(stock)
        ):

            return StrategyResult(
                strategy=self.name,
                signal="BUY",
                confidence=80.0,
                reason="Bullish MACD crossover above zero line (ADX + VWAP confirmed)",
                price=float(tick.ltp),
            )

        #
        # SELL
        #
        if (
                indicator.macd < indicator.macd_signal
                and indicator.macd_histogram < 0
                and indicator.macd < 0
                and StrategyFilters.adx_bearish(stock)
                and StrategyFilters.below_vwap(stock)
        ):

            return StrategyResult(
                strategy=self.name,
                signal="SELL",
                confidence=80.0,
                reason="Bearish MACD crossover below zero line (ADX + VWAP confirmed)",
                price=float(tick.ltp),
            )

        return None