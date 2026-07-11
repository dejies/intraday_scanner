"""
ADX Engine.

Responsibilities
----------------
- Calculate ADX(14)
- No database access
- No repository access
- No service logic
"""

from __future__ import annotations

from decimal import Decimal

from src.models.candle import Candle


class ADXEngine:
    """
    Average Directional Index.
    """

    @staticmethod
    def calculate(
        candles: list[Candle],
        period: int = 14,
    ) -> float | None:

        if len(candles) < (period * 2):
            return None

        tr_list = []
        plus_dm_list = []
        minus_dm_list = []

        for i in range(1, len(candles)):

            current = candles[i]
            previous = candles[i - 1]

            high_diff = current.high - previous.high
            low_diff = previous.low - current.low

            plus_dm = (
                high_diff
                if high_diff > low_diff and high_diff > 0
                else Decimal("0")
            )

            minus_dm = (
                low_diff
                if low_diff > high_diff and low_diff > 0
                else Decimal("0")
            )

            tr = max(
                current.high - current.low,
                abs(current.high - previous.close),
                abs(current.low - previous.close),
            )

            tr_list.append(tr)
            plus_dm_list.append(plus_dm)
            minus_dm_list.append(minus_dm)

        dx_values = []

        for i in range(period, len(tr_list) + 1):

            tr14 = sum(tr_list[i - period:i])

            if tr14 == 0:
                continue

            plus14 = sum(
                plus_dm_list[i - period:i]
            )

            minus14 = sum(
                minus_dm_list[i - period:i]
            )

            plus_di = (
                Decimal("100")
                * plus14
                / tr14
            )

            minus_di = (
                Decimal("100")
                * minus14
                / tr14
            )

            denominator = plus_di + minus_di

            if denominator == 0:
                continue

            dx = (
                abs(
                    plus_di - minus_di
                )
                / denominator
            ) * Decimal("100")

            dx_values.append(dx)

        if len(dx_values) < period:
            return None

        adx = (
            sum(dx_values[-period:])
            / Decimal(period)
        )

        return round(float(adx), 2)