"""
Signal Analysis Engine.

Combines facts from all analyzers.
"""

from __future__ import annotations

from src.analysis.analysis_fact import (
    AnalysisFact,
    AnalysisFactType,
)
from src.analysis.trend_analyzer import TrendAnalyzer
from src.analysis.momentum_analyzer import MomentumAnalyzer
from src.analysis.volume_analyzer import VolumeAnalyzer
from src.analysis.price_analyzer import PriceAnalyzer
from src.core.market_data_store import StockState


class SignalAnalysisEngine:

    def __init__(self):

        self._trend = TrendAnalyzer()

        self._momentum = MomentumAnalyzer()

        self._volume = VolumeAnalyzer()

        self._price = PriceAnalyzer()

    # ---------------------------------------------------------

    def analyze(
        self,
        stock: StockState,
    ) -> list[AnalysisFact]:

        facts: list[AnalysisFact] = []

        facts.extend(
            self._trend.analyze(stock)
        )

        facts.extend(
            self._momentum.analyze(stock)
        )

        facts.extend(
            self._volume.analyze(stock)
        )

        facts.extend(
            self._price.analyze(stock)
        )

        #
        # Remove duplicates.
        #
        unique = {}

        for fact in facts:

            unique[fact.type] = fact

        return list(unique.values())