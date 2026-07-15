"""
Volume Analyzer.
"""

from __future__ import annotations

from src.analysis.analysis_fact import (
    AnalysisFact,
    AnalysisFactType,
)
from src.core.market_data_store import StockState


class VolumeAnalyzer:

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
        # Relative Volume
        #
        if (
            indicator.relative_volume is not None
            and indicator.relative_volume >= 1.5
        ):

            facts.append(
                AnalysisFact(
                    type=AnalysisFactType.RVOL_HIGH,
                    description=(
                        f"Relative Volume "
                        f"{indicator.relative_volume:.2f}"
                    ),
                    value=indicator.relative_volume,
                )
            )

        #
        # VWAP
        #
        if indicator.vwap is not None:

            if float(tick.ltp) > indicator.vwap:

                facts.append(
                    AnalysisFact(
                        type=AnalysisFactType.ABOVE_VWAP,
                        description="Price Above VWAP",
                        value=indicator.vwap,
                    )
                )

            elif float(tick.ltp) < indicator.vwap:

                facts.append(
                    AnalysisFact(
                        type=AnalysisFactType.BELOW_VWAP,
                        description="Price Below VWAP",
                        value=indicator.vwap,
                    )
                )

        return facts