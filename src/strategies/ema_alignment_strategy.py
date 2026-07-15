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
from src.strategies.strategy_filters import StrategyFilters
from src.strategies.evidence import (
    EvidenceType,
    SignalEvidence,
)

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
            and StrategyFilters.adx_bullish(stock)
            and StrategyFilters.above_vwap(stock)
        ):
            return StrategyResult(
                strategy=self.name,
                signal="BUY",
                confidence=82.0,  # temporary
                reason="Bullish EMA alignment (ADX confirmed)",
                price=float(tick.ltp),
                evidence=[
                    SignalEvidence(
                        strategy=self.name,
                        signal="BUY",
                        evidence=EvidenceType.EMA_ALIGNMENT,
                        description="EMA9 > EMA20 > EMA50 > EMA200",
                    ),
                    SignalEvidence(
                        strategy=self.name,
                        signal="BUY",
                        evidence=EvidenceType.ADX_STRONG,
                        description="ADX confirms trend",
                    ),
                    SignalEvidence(
                        strategy=self.name,
                        signal="BUY",
                        evidence=EvidenceType.ABOVE_VWAP,
                        description="Price above VWAP",
                    ),
                ],
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
            and StrategyFilters.adx_bearish(stock)
            and StrategyFilters.below_vwap(stock)
        ):
            return StrategyResult(
                strategy=self.name,
                signal="SELL",
                confidence=82.0,
                reason="Bearish EMA alignment (ADX confirmed)",
                price=float(tick.ltp),
                evidence=[
                    SignalEvidence(
                        strategy=self.name,
                        signal="SELL",
                        evidence=EvidenceType.EMA_ALIGNMENT,
                        description="EMA9 < EMA20 < EMA50 < EMA200",
                    ),
                    SignalEvidence(
                        strategy=self.name,
                        signal="SELL",
                        evidence=EvidenceType.ADX_STRONG,
                        description="ADX confirms trend",
                    ),
                    SignalEvidence(
                        strategy=self.name,
                        signal="SELL",
                        evidence=EvidenceType.BELOW_VWAP,
                        description="Price below VWAP",
                    ),
                ],
            )

        return None