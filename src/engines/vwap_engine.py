"""
VWAP Engine.

Responsibilities
----------------
- Calculate intraday VWAP
- No database access
- No repository access
- No service logic
"""

from __future__ import annotations

from decimal import Decimal

from src.models.candle import Candle


class VWAPEngine:
    """
    Volume Weighted Average Price.
    """

    @staticmethod
    def calculate(
        candles: list[Candle],
    ) -> float | None:
        """
        Calculate today's VWAP.
        """

        if not candles:
            return None

        trading_day = candles[-1].candle_time.date()

        day_candles = [
            candle
            for candle in candles
            if candle.candle_time.date() == trading_day
        ]

        if not day_candles:
            return None

        total_price_volume = Decimal("0")
        total_volume = Decimal("0")

        for candle in day_candles:

            typical_price = (
                candle.high +
                candle.low +
                candle.close
            ) / Decimal("3")

            total_price_volume += (
                typical_price *
                Decimal(candle.volume)
            )

            total_volume += Decimal(candle.volume)

        if total_volume == 0:
            return None

        vwap = total_price_volume / total_volume

        return round(float(vwap), 2)