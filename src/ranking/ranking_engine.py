"""
Ranking Engine.
"""

from __future__ import annotations

from src.models.signal import Signal
from src.models.enums import SignalType
from src.ranking.ranking_config import RankingConfig
from src.ranking.ranked_signal import RankedSignal


class RankingEngine:

    def __init__(
        self,
        config: RankingConfig | None = None,
    ):

        self._config = (
            config
            if config is not None
            else RankingConfig()
        )

    def rank(
        self,
        signals: list[Signal],
    ) -> list[RankedSignal]:
        ranked = sorted(
            signals,
            key=lambda s: (
                s.score_percentage,
                s.raw_score,
                s.confidence,
                s.timestamp,
            ),
            reverse=True,
        )

        results = []

        for index, signal in enumerate(

            ranked,

            start=1,

        ):

            results.append(

                RankedSignal(

                    signal=signal,

                    rank=index,

                    score=signal.confidence,

                )

            )

        return results

    def rank_buy(
            self,
            signals: list[Signal],
    ) -> list[RankedSignal]:
        buy = [
            s
            for s in signals
            if s.signal_type == SignalType.BUY
        ]

        ranked = self.rank(buy)

        ranked = [
            item
            for item in ranked
            if item.score >= self._config.minimum_score
        ]

        return ranked[
            : self._config.max_buy_signals
        ]

    def rank_sell(
            self,
            signals: list[Signal],
    ) -> list[RankedSignal]:
        sell = [
            s
            for s in signals
            if s.signal_type == SignalType.SELL
        ]

        ranked = self.rank(sell)

        ranked = [
            item
            for item in ranked
            if item.score >= self._config.minimum_score
        ]

        return ranked[
            : self._config.max_sell_signals
        ]