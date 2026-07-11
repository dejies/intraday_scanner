"""
MACD Engine.

Responsibilities
----------------
- Calculate MACD
- Calculate Signal Line
- Calculate Histogram
- No database access
- No repository access
- No service logic
"""

from __future__ import annotations

from src.models.candle import Candle
from src.engines.ema_engine import EMAEngine


class MACDEngine:
    """
    Moving Average Convergence Divergence.
    """

    FAST_PERIOD = 12
    SLOW_PERIOD = 26
    SIGNAL_PERIOD = 9

    @staticmethod
    def calculate(
        candles: list[Candle],
    ) -> tuple[float | None, float | None, float | None]:
        """
        Returns:
            (
                macd,
                signal,
                histogram
            )
        """

        if len(candles) < (
            MACDEngine.SLOW_PERIOD +
            MACDEngine.SIGNAL_PERIOD
        ):
            return None, None, None

        ema12_values = []
        ema26_values = []

        for i in range(
            MACDEngine.FAST_PERIOD,
            len(candles) + 1,
        ):
            value = EMAEngine.calculate(
                candles[:i],
                MACDEngine.FAST_PERIOD,
            )

            if value is not None:
                ema12_values.append(value)

        for i in range(
            MACDEngine.SLOW_PERIOD,
            len(candles) + 1,
        ):
            value = EMAEngine.calculate(
                candles[:i],
                MACDEngine.SLOW_PERIOD,
            )

            if value is not None:
                ema26_values.append(value)

        length = min(
            len(ema12_values),
            len(ema26_values),
        )

        ema12_values = ema12_values[-length:]
        ema26_values = ema26_values[-length:]

        macd_series = [
            round(e12 - e26, 2)
            for e12, e26 in zip(
                ema12_values,
                ema26_values,
            )
        ]

        if len(macd_series) < MACDEngine.SIGNAL_PERIOD:
            return (
                macd_series[-1],
                None,
                None,
            )

        multiplier = (
            2 /
            (MACDEngine.SIGNAL_PERIOD + 1)
        )

        signal = (
            sum(
                macd_series[
                    :MACDEngine.SIGNAL_PERIOD
                ]
            )
            / MACDEngine.SIGNAL_PERIOD
        )

        for value in macd_series[
            MACDEngine.SIGNAL_PERIOD:
        ]:
            signal = (
                (value - signal)
                * multiplier
            ) + signal

        macd = macd_series[-1]

        signal = round(signal, 2)

        histogram = round(
            macd - signal,
            2,
        )

        return (
            macd,
            signal,
            histogram,
        )