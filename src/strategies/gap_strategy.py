"""
Gap Up / Gap Down trading strategy.
"""

from __future__ import annotations

from src.core.market_data_store import StockState
from src.services.gap_service import GapService
from src.strategies.base_strategy import BaseStrategy
from src.strategies.strategy_filters import StrategyFilters
from src.strategies.strategy_result import StrategyResult
from src.models.gap import GapDirection


class GapStrategy(BaseStrategy):

    def __init__(
        self,
        gap_service: GapService,
    ):

        super().__init__("Gap Continuation")

        self._gap_service = gap_service

    # ---------------------------------------------------------

    def evaluate(
        self,
        stock: StockState,
    ) -> StrategyResult | None:

        indicator = stock.indicator
        tick = stock.tick

        if indicator is None or tick is None:
            return None

        gap = self._gap_service.get(
            stock.instrument.security_id
        )

        if gap is None:
            return None

        #
        # BUY
        #
        if (
            gap.direction == GapDirection.UP
            and not gap.buy_triggered
            and tick.ltp > gap.today_open
            and StrategyFilters.adx_bullish(stock)
            and StrategyFilters.above_vwap(stock)
        ):

            gap.buy_triggered = True

            return StrategyResult(
                strategy=self.name,
                signal="BUY",
                confidence=78.0,
                reason=f"Gap Up {gap.gap_percent:.2f}% confirmed",
                price=float(tick.ltp),
            )

        #
        # SELL
        #
        if (
            gap.direction == GapDirection.DOWN
            and not gap.sell_triggered
            and tick.ltp < gap.today_open
            and StrategyFilters.adx_bearish(stock)
            and StrategyFilters.below_vwap(stock)
        ):

            gap.sell_triggered = True

            return StrategyResult(
                strategy=self.name,
                signal="SELL",
                confidence=78.0,
                reason=f"Gap Down {abs(gap.gap_percent):.2f}% confirmed",
                price=float(tick.ltp),
            )

        return None