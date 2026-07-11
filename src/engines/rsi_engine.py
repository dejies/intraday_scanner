"""
Relative Strength Index (RSI) Engine.

Responsibilities
----------------
- Calculate RSI values
- No database access
- No repository access
- No service logic
"""

from __future__ import annotations

from decimal import Decimal

from src.models.candle import Candle


class RSIEngine:
    """
    Relative Strength Index calculator.
    """

    @staticmethod
    def calculate(
        candles: list[Candle],
        period: int = 14,
    ) -> float | None:
        """
        Calculate RSI from candle history.
        """

        if len(candles) < period + 1:
            return None

        recent = candles[-(period + 1):]

        gains: list[Decimal] = []
        losses: list[Decimal] = []

        for i in range(1, len(recent)):

            change = (
                recent[i].close
                - recent[i - 1].close
            )

            if change > 0:
                gains.append(change)
                losses.append(Decimal("0"))
            else:
                gains.append(Decimal("0"))
                losses.append(abs(change))

        average_gain = sum(gains) / Decimal(period)
        average_loss = sum(losses) / Decimal(period)

        if average_loss == 0:
            return 100.0

        rs = average_gain / average_loss

        rsi = Decimal("100") - (
            Decimal("100") / (Decimal("1") + rs)
        )

        return round(float(rsi), 2)

    @staticmethod
    def rsi14(
        candles: list[Candle],
    ) -> float | None:
        """
        Convenience method for RSI(14).
        """
        return RSIEngine.calculate(candles, 14)