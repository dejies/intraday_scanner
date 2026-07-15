"""
Trend Analyzer.

Produces trend-related analysis facts.
"""

from __future__ import annotations

from src.analysis.analysis_fact import (
    AnalysisFact,
    AnalysisFactType,
)
from src.core.market_data_store import StockState


class TrendAnalyzer:

    def analyze(
        self,
        stock: StockState,
    ) -> list[AnalysisFact]:

        facts: list[AnalysisFact] = []

        indicator = stock.indicator
        tick = stock.tick

        if indicator is None or tick is None:
            return facts

        #
        # Required indicators
        #
        required = (
            indicator.ema9,
            indicator.ema20,
            indicator.ema50,
            indicator.ema200,
            indicator.adx14,
        )

        if any(value is None for value in required):
            return facts

        #
        # Bullish EMA Alignment
        #
        if (
            indicator.ema9 >
            indicator.ema20 >
            indicator.ema50 >
            indicator.ema200
        ):

            facts.append(
                AnalysisFact(
                    type=AnalysisFactType.EMA_ALIGNMENT,
                    description="Bullish EMA Alignment",
                )
            )

        #
        # Bearish EMA Alignment
        #
        elif (
            indicator.ema9 <
            indicator.ema20 <
            indicator.ema50 <
            indicator.ema200
        ):

            if (
                    indicator.ema9 > indicator.ema20 >
                    indicator.ema50 > indicator.ema200
            ):

                facts.append(
                    AnalysisFact(
                        type=AnalysisFactType.EMA_BULLISH_ALIGNMENT,
                        description="Bullish EMA Alignment",
                    )
                )

            elif (
                    indicator.ema9 < indicator.ema20 <
                    indicator.ema50 < indicator.ema200
            ):

                facts.append(
                    AnalysisFact(
                        type=AnalysisFactType.EMA_BEARISH_ALIGNMENT,
                        description="Bearish EMA Alignment",
                    )
                )

        #
        # ADX
        #
        if indicator.adx14 >= 20:
            AnalysisFact(
                type=AnalysisFactType.ADX_STRONG,
                description="ADX Strong",
                value=indicator.adx14,
            )

        #
        # Price vs EMA20
        #
        if tick.ltp > indicator.ema20:

            facts.append(
                AnalysisFact(
                    type=AnalysisFactType.PRICE_ABOVE_EMA20,
                    description="Price Above EMA20",
                )
            )

        elif tick.ltp < indicator.ema20:

            facts.append(
                AnalysisFact(
                    type=AnalysisFactType.PRICE_BELOW_EMA20,
                    description="Price Below EMA20",
                )
            )

        return facts