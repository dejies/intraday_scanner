"""
RSI trading strategy.
"""

from __future__ import annotations

from src.core.market_data_store import StockState
from src.strategies.base_strategy import BaseStrategy
from src.strategies.strategy_result import StrategyResult
from src.strategies.strategy_filters import StrategyFilters

class RSIStrategy(BaseStrategy):

    BUY_RSI = 60.0
    SELL_RSI = 40.0

    def __init__(self):

        super().__init__("RSI Momentum")

    # ---------------------------------------------------------

    def evaluate(
        self,
        stock: StockState,
    ) -> StrategyResult | None:

        indicator = stock.indicator
        tick = stock.tick

        if indicator is None or tick is None:
            return None

        if indicator.rsi14 is None:
            return None

        #
        # BUY
        #
        if (
                indicator.rsi14 >= self.BUY_RSI
                and StrategyFilters.adx_bullish(stock)
                and StrategyFilters.above_vwap(stock)
        ):

            return StrategyResult(
                strategy=self.name,
                signal="BUY",
                confidence=72.0,
                reason=f"RSI {indicator.rsi14:.2f} above {self.BUY_RSI} (ADX + VWAP confirmed)",
                price=float(tick.ltp),
            )

        #
        # SELL
        #
        if (
                indicator.rsi14 <= self.SELL_RSI
                and StrategyFilters.adx_bearish(stock)
                and StrategyFilters.below_vwap(stock)
        ):

            return StrategyResult(
                strategy=self.name,
                signal="SELL",
                confidence=72.0,
                reason=f"RSI {indicator.rsi14:.2f} below {self.SELL_RSI} (ADX + VWAP confirmed)",
                price=float(tick.ltp),
            )

        return None