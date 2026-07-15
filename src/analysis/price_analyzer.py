"""
Price Analyzer.
"""

from __future__ import annotations

from src.analysis.analysis_fact import (
    AnalysisFact,
    AnalysisFactType,
)
from src.core.market_data_store import StockState


class PriceAnalyzer:

    #
    # Within 0.5%
    #
    EMA_THRESHOLD = 0.005

    def analyze(
            self,
            stock: StockState,
    ) -> list[AnalysisFact]:

        facts: list[AnalysisFact] = []

        indicator = stock.indicator
        tick = stock.tick

        if indicator is None or tick is None:
            return facts

        ltp = float(tick.ltp)

        nearest_fact = None
        nearest_distance = None

        #
        # EMA20
        #
        if indicator.ema20 is not None:

            distance = abs(
                ltp - indicator.ema20
            ) / indicator.ema20

            if distance <= self.EMA_THRESHOLD:
                nearest_distance = distance

                nearest_fact = AnalysisFact(
                    type=AnalysisFactType.PRICE_NEAR_EMA20,
                    description=(
                        f"Price Near EMA20 "
                        f"({distance * 100:.2f}%)"
                    ),
                )

        #
        # EMA50
        #
        if indicator.ema50 is not None:

            distance = abs(
                ltp - indicator.ema50
            ) / indicator.ema50

            if distance <= self.EMA_THRESHOLD:

                if (
                        nearest_distance is None
                        or distance < nearest_distance
                ):
                    nearest_distance = distance

                    nearest_fact = AnalysisFact(
                        type=AnalysisFactType.PRICE_NEAR_EMA50,
                        description=(
                            f"Price Near EMA50 "
                            f"({distance * 100:.2f}%)"
                        ),
                    )

        if nearest_fact is not None:
            facts.append(nearest_fact)

        return facts