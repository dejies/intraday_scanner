"""
Technical Indicator Engine

Calculates all technical indicators from candle history.

This is the single source of truth for indicators.
"""

from __future__ import annotations

from src.models.candle import Candle
from src.models.indicator import IndicatorData


class IndicatorEngine:
    """
    Calculates technical indicators for one symbol.
    """

    def calculate(
            self,
            symbol: str,
            candles: list[Candle],
    ) -> IndicatorData:
        """
        Calculate all technical indicators.
        """

        if not candles:
            raise ValueError(
                f"No candles available for {symbol}"
            )

        latest = candles[-1]

        #
        # Trend
        #
        ema20 = self._ema(
            candles,
            20,
        )

        ema50 = self._ema(
            candles,
            50,
        )

        #
        # Momentum
        #
        rsi14 = self._rsi(
            candles,
            14,
        )

        #
        # Intraday
        #
        vwap = self._vwap(
            candles,
        )

        #
        # Volume
        #
        average_volume20 = self._average_volume(
            candles,
            20,
        )

        relative_volume = self._relative_volume(
            candles,
            average_volume20,
        )

        return IndicatorData(

            #
            # Latest Price
            #
            ltp=latest.close,

            #
            # Trend
            #
            ema20=ema20,
            ema50=ema50,

            #
            # Momentum
            #
            rsi14=rsi14,

            #
            # Intraday
            #
            vwap=vwap,

            #
            # Volatility
            #
            atr14=None,

            #
            # Volume
            #
            average_volume20=average_volume20,
            relative_volume=relative_volume,
        )

    def _ema(
            self,
            candles: list[Candle],
            period: int,
    ) -> float | None:
        """
        Calculate Exponential Moving Average.
        """

        if len(candles) < period:
            return None

        multiplier = 2 / (period + 1)

        #
        # Initial EMA uses SMA.
        #
        ema = (
                sum(
                    candle.close
                    for candle in candles[:period]
                )
                / period
        )

        #
        # Remaining candles.
        #
        for candle in candles[period:]:
            ema = (
                          (candle.close - ema)
                          * multiplier
                  ) + ema

        return round(
            ema,
            2,
        )

    def _average_volume(
            self,
            candles: list[Candle],
            period: int,
    ) -> float | None:
        """
        Calculate average volume.
        """

        if len(candles) < period:
            return None

        return (
                sum(
                    candle.volume
                    for candle in candles[-period:]
                )
                / period
        )

    def _relative_volume(
            self,
            candles: list[Candle],
            average_volume: float | None,
    ) -> float | None:
        """
        Calculate Relative Volume (RVOL).
        """

        if average_volume is None:
            return None

        if average_volume == 0:
            return None

        current_volume = candles[-1].volume

        return round(
            current_volume / average_volume,
            2,
        )

    def _rsi(
            self,
            candles: list[Candle],
            period: int,
    ) -> float | None:
        """
        Calculate Relative Strength Index (RSI).
        """

        if len(candles) < period + 1:
            return None

        recent = candles[-(period + 1):]

        gains = []
        losses = []

        for i in range(1, len(recent)):

            change = (
                    recent[i].close
                    - recent[i - 1].close
            )

            if change > 0:

                gains.append(change)
                losses.append(0)

            else:

                gains.append(0)
                losses.append(abs(change))

        average_gain = sum(gains) / period
        average_loss = sum(losses) / period

        if average_loss == 0:
            return 100.0

        rs = average_gain / average_loss

        rsi = 100 - (
                100 / (1 + rs)
        )

        return round(
            rsi,
            2,
        )

    def _vwap(
            self,
            candles: list[Candle],
    ) -> float | None:
        """
        Calculate today's VWAP.
        """

        if not candles:
            return None

        today = candles[-1].timestamp.date()

        todays_candles = [
            candle
            for candle in candles
            if candle.timestamp.date() == today
        ]

        if not todays_candles:
            return None

        total_price_volume = 0.0
        total_volume = 0

        for candle in todays_candles:
            typical_price = (
                                    candle.high
                                    + candle.low
                                    + candle.close
                            ) / 3

            total_price_volume += (
                    typical_price
                    * candle.volume
            )

            total_volume += candle.volume

        if total_volume == 0:
            return None

        return round(
            total_price_volume / total_volume,
            2,
        )


def highest_high(
        candles: list[Candle],
        period: int,
) -> float | None:
    """
    Return the highest high over the period.
    """

    if len(candles) < period:
        return None

    return max(
        candle.high
        for candle in candles[-period:]
    )

def lowest_low(
        candles: list[Candle],
        period: int,
) -> float | None:
    """
    Return the lowest low over the period.
    """

    if len(candles) < period:
        return None

    return min(
        candle.low
        for candle in candles[-period:]
    )

def average_volume(
        candles: list[Candle],
        period: int,
) -> float | None:
    """
    Return average volume over the period.
    """

    if len(candles) < period:
        return None

    return (
            sum(
                candle.volume
                for candle in candles[-period:]
            )
            / period
    )