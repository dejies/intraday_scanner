"""
Momentum Analyzer.
"""

from __future__ import annotations

from src.analysis.analysis_fact import (
    AnalysisFact,
    AnalysisFactType,
)
from src.core.market_data_store import StockState


class MomentumAnalyzer:

    def analyze(
        self,
        stock: StockState,
    ) -> list[AnalysisFact]:

        facts: list[AnalysisFact] = []

        indicator = stock.indicator

        if indicator is None:
            return facts

        #
        # RSI
        #
        if indicator.rsi14 is not None:

            if indicator.rsi14 >= 60:

                facts.append(
                    AnalysisFact(
                        type=AnalysisFactType.RSI_BULLISH,
                        description=f"RSI {indicator.rsi14:.2f}",
                        value=indicator.rsi14,
                    )
                )

            elif indicator.rsi14 <= 40:

                facts.append(
                    AnalysisFact(
                        type=AnalysisFactType.RSI_BEARISH,
                        description=f"RSI {indicator.rsi14:.2f}",
                        value=indicator.rsi14,
                    )
                )

        #
        # MACD
        #
        if (
            indicator.macd is not None
            and indicator.macd_signal is not None
        ):

            if indicator.macd > indicator.macd_signal:

                facts.append(
                    AnalysisFact(
                        type=AnalysisFactType.MACD_BULLISH,
                        description="MACD Bullish Crossover",
                        value=indicator.macd,
                    )
                )

            elif indicator.macd < indicator.macd_signal:

                facts.append(
                    AnalysisFact(
                        type=AnalysisFactType.MACD_BEARISH,
                        description="MACD Bearish Crossover",
                        value=indicator.macd,
                    )
                )

        return facts