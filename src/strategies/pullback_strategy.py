"""
Trend Pullback strategy.
"""

from __future__ import annotations

from src.core.market_data_store import StockState
from src.strategies.base_strategy import BaseStrategy
from src.strategies.strategy_filters import StrategyFilters
from src.strategies.strategy_result import StrategyResult


class PullbackStrategy(BaseStrategy):

    def __init__(self):

        super().__init__("Trend Pullback")

    # ---------------------------------------------------------

    def evaluate(
        self,
        stock: StockState,
    ) -> StrategyResult | None:

        indicator = stock.indicator
        tick = stock.tick

        if indicator is None or tick is None:
            return None

        #
        # Ensure required indicators exist
        #
        required = (
            indicator.ema9,
            indicator.ema20,
            indicator.ema50,
            indicator.ema200,
            indicator.rsi14,
            indicator.macd,
            indicator.macd_signal,
            indicator.adx14,
            indicator.vwap,
        )

        if any(value is None for value in required):
            return None

        #
        # BUY Pullback
        #
        if (
            indicator.ema9 > indicator.ema20 > indicator.ema50 > indicator.ema200
            and indicator.ema20 <= tick.ltp <= indicator.ema9
            and tick.ltp > indicator.ema50
            and indicator.rsi14 > 55
            and indicator.macd > indicator.macd_signal
            and StrategyFilters.adx_bullish(stock)
            and StrategyFilters.above_vwap(stock)
        ):

            return StrategyResult(
                strategy=self.name,
                signal="BUY",
                confidence=88.0,
                reason="Bullish pullback in strong uptrend",
                price=float(tick.ltp),
            )

        #
        # SELL Pullback
        #
        if (
            indicator.ema9 < indicator.ema20 < indicator.ema50 < indicator.ema200
            and indicator.ema9 <= tick.ltp <= indicator.ema20
            and tick.ltp < indicator.ema50
            and indicator.rsi14 < 45
            and indicator.macd < indicator.macd_signal
            and StrategyFilters.adx_bearish(stock)
            and StrategyFilters.below_vwap(stock)
        ):

            return StrategyResult(
                strategy=self.name,
                signal="SELL",
                confidence=88.0,
                reason="Bearish pullback in strong downtrend",
                price=float(tick.ltp),
            )

        return None