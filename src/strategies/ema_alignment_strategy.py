"""
EMA Alignment trading strategy.

BUY
----
EMA9 > EMA20 > EMA50 > EMA200

SELL
-----
EMA9 < EMA20 < EMA50 < EMA200
"""

from __future__ import annotations

from src.core.market_data_store import StockState
from src.strategies.base_strategy import BaseStrategy
from src.strategies.strategy_result import StrategyResult


class EMAAlignmentStrategy(BaseStrategy):

    def __init__(self):

        super().__init__("EMA Alignment")

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
            indicator.ema9 is None
            or indicator.ema20 is None
            or indicator.ema50 is None
            or indicator.ema200 is None
        ):
            return None

        #
        # BUY
        #
        if (
            indicator.ema9
            > indicator.ema20
            > indicator.ema50
            > indicator.ema200
            and tick.ltp > indicator.ema9
        ):

            return StrategyResult(
                strategy=self.name,
                signal="BUY",
                confidence=75.0,
                reason="Bullish EMA alignment",
                price=float(tick.ltp),
            )

        #
        # SELL
        #
        if (
            indicator.ema9
            < indicator.ema20
            < indicator.ema50
            < indicator.ema200
            and tick.ltp < indicator.ema9
        ):

            return StrategyResult(
                strategy=self.name,
                signal="SELL",
                confidence=75.0,
                reason="Bearish EMA alignment",
                price=float(tick.ltp),
            )

        return None