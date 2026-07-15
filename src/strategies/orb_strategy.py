"""
Opening Range Breakout strategy.
"""

from __future__ import annotations

from src.core.market_data_store import StockState
from src.services.opening_range_service import OpeningRangeService
from src.strategies.base_strategy import BaseStrategy
from src.strategies.strategy_filters import StrategyFilters
from src.strategies.strategy_result import StrategyResult


class ORBStrategy(BaseStrategy):

    def __init__(
        self,
        opening_range_service: OpeningRangeService,
    ):

        super().__init__("Opening Range Breakout")

        self._opening_range_service = opening_range_service

    # ---------------------------------------------------------

    def evaluate(
        self,
        stock: StockState,
    ) -> StrategyResult | None:

        indicator = stock.indicator
        tick = stock.tick

        if indicator is None or tick is None:
            return None

        orb = self._opening_range_service.get(
            stock.instrument.security_id
        )

        if orb is None:
            return None

        if not orb.locked:
            return None

        #
        # BUY
        #
        if (
            tick.ltp > orb.high
            and not orb.buy_triggered
            and StrategyFilters.adx_bullish(stock)
            and StrategyFilters.above_vwap(stock)
        ):
            orb.buy_triggered = True
            return StrategyResult(
                strategy=self.name,
                signal="BUY",
                confidence=self._confidence(stock),
                reason="Opening Range Breakout (Bullish)",
                price=float(tick.ltp),
            )

        #
        # SELL
        #
        if (
            tick.ltp < orb.low
            and StrategyFilters.adx_bearish(stock)
            and StrategyFilters.below_vwap(stock)
        ):

            return StrategyResult(
                strategy=self.name,
                signal="SELL",
                confidence=self._confidence(stock),
                reason="Opening Range Breakout (Bearish)",
                price=float(tick.ltp),
            )

        return None

    def _confidence(
            self,
            stock: StockState,
    ) -> float:

        indicator = stock.indicator
        tick = stock.tick

        score = 60.0

        #
        # Strong trend
        #
        if indicator.adx14 is not None and indicator.adx14 >= 25:
            score += 10

        #
        # Above / Below VWAP
        #
        if (
                indicator.vwap is not None
                and abs(float(tick.ltp) - float(indicator.vwap)) > 0
        ):
            score += 5

        #
        # EMA alignment
        #
        if (
                indicator.ema9
                and indicator.ema20
                and indicator.ema50
                and indicator.ema200
        ):

            if (
                    indicator.ema9 >
                    indicator.ema20 >
                    indicator.ema50 >
                    indicator.ema200
            ):
                score += 10

            elif (
                    indicator.ema9 <
                    indicator.ema20 <
                    indicator.ema50 <
                    indicator.ema200
            ):
                score += 10

        #
        # MACD confirmation
        #
        if (
                indicator.macd is not None
                and indicator.macd_signal is not None
        ):

            if indicator.macd > indicator.macd_signal:
                score += 5

            elif indicator.macd < indicator.macd_signal:
                score += 5

        #
        # RSI confirmation
        #
        if indicator.rsi14 is not None:

            if indicator.rsi14 >= 60:
                score += 5

            elif indicator.rsi14 <= 40:
                score += 5

        return min(score, 100.0)