"""
Signal Ranking

Ranks and filters trading signals.
"""

from __future__ import annotations

from src.models.signal import Signal


class SignalRanking:

    def rank(
        self,
        signals: list[Signal],
    ) -> list[Signal]:
        """
        Rank trading signals.

        1. Remove duplicates.
        2. Sort by confidence.
        """

        unique = {}

        for signal in signals:

            key = (
                signal.symbol,
                signal.signal,
            )

            existing = unique.get(key)

            if (
                existing is None
                or signal.confidence > existing.confidence
            ):
                unique[key] = signal

        ranked = sorted(
            unique.values(),
            key=lambda s: s.confidence,
            reverse=True,
        )

        return ranked