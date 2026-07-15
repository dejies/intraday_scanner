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
            and StrategyFilters.adx_bullish(stock)
            and StrategyFilters.above_vwap(stock)
        ):

            return StrategyResult(
                strategy=self.name,
                signal="BUY",
                confidence=85.0,
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
                confidence=85.0,
                reason="Opening Range Breakout (Bearish)",
                price=float(tick.ltp),
            )

        return None