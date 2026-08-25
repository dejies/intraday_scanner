"""
Average True Range (ATR) Engine.
"""

from __future__ import annotations

from src.models.candle import Candle


class ATREngine:
    """
    Calculates Average True Range (ATR).

    ATR is a measure of volatility.

    Uses Wilder's ATR formula.
    """

    PERIOD = 14

    @classmethod
    def calculate(
        cls,
        candles: list[Candle],
    ) -> float | None:

        #
        # Need previous close for first TR.
        #
        if len(candles) < cls.PERIOD + 1:
            return None

        true_ranges = []

        #
        # Calculate True Range
        #
        for i in range(1, len(candles)):

            current = candles[i]
            previous = candles[i - 1]

            tr = max(
                current.high - current.low,
                abs(current.high - previous.close),
                abs(current.low - previous.close),
            )

            true_ranges.append(tr)

        #
        # Wilder ATR
        #
        atr = (
            sum(true_ranges[-cls.PERIOD:])
            / cls.PERIOD
        )

        return round(atr, 2)