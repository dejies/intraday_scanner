"""
Exponential Moving Average (EMA) Engine.

Responsibilities
----------------
- Calculate EMA values
- Support full-history calculation
- Support incremental calculation
- No database access
- No repository access
- No service logic
"""

from __future__ import annotations

from decimal import Decimal

from src.models.candle import Candle


class EMAEngine:
    """
    Exponential Moving Average calculator.
    """

    @staticmethod
    def calculate(
        candles: list[Candle],
        period: int,
    ) -> float | None:
        """
        Calculate EMA from complete candle history.
        """

        if len(candles) < period:
            return None

        multiplier = Decimal("2") / Decimal(period + 1)

        ema = (
            sum(
                candle.close
                for candle in candles[:period]
            )
            / Decimal(period)
        )

        for candle in candles[period:]:
            ema = (
                (candle.close - ema) * multiplier
            ) + ema

        return round(float(ema), 2)

    @staticmethod
    def update(
        previous_ema: float,
        latest_close: Decimal,
        period: int,
    ) -> float:
        """
        Incrementally calculate the next EMA.

        Formula:
            EMA = (Close - PreviousEMA) * Multiplier + PreviousEMA
        """

        multiplier = Decimal("2") / Decimal(period + 1)

        ema = (
            (latest_close - Decimal(str(previous_ema)))
            * multiplier
        ) + Decimal(str(previous_ema))

        return round(float(ema), 2)

    @staticmethod
    def ema9(
        candles: list[Candle],
    ) -> float | None:
        return EMAEngine.calculate(candles, 9)

    @staticmethod
    def ema20(
        candles: list[Candle],
    ) -> float | None:
        return EMAEngine.calculate(candles, 20)

    @staticmethod
    def ema50(
        candles: list[Candle],
    ) -> float | None:
        return EMAEngine.calculate(candles, 50)

    @staticmethod
    def ema200(
        candles: list[Candle],
    ) -> float | None:
        return EMAEngine.calculate(candles, 200)