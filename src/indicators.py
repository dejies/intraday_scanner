"""
Technical Indicators

All functions accept a list of Candle objects.
"""

from __future__ import annotations

from src.models.candle import Candle


def sma(candles: list[Candle], period: int) -> float | None:
    """
    Simple Moving Average.
    """
    if len(candles) < period:
        return None

    closes = [c.close for c in candles[-period:]]

    return sum(closes) / period


def ema(candles: list[Candle], period: int) -> float | None:
    """
    Exponential Moving Average.
    """

    if len(candles) < period:
        return None

    closes = [c.close for c in candles]

    multiplier = 2 / (period + 1)

    ema_value = sum(closes[:period]) / period

    for close in closes[period:]:
        ema_value = ((close - ema_value) * multiplier) + ema_value

    return ema_value


def highest_high(
    candles: list[Candle],
    period: int,
) -> float | None:
    """
    Highest High
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
    Lowest Low
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
    Average traded volume.
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


def vwap(
    candles: list[Candle],
) -> float | None:
    """
    Volume Weighted Average Price.
    """

    if not candles:
        return None

    total_price_volume = 0.0
    total_volume = 0

    for candle in candles:

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

    return total_price_volume / total_volume


def rsi(
    candles: list[Candle],
    period: int = 14,
) -> float | None:
    """
    Relative Strength Index.
    """

    if len(candles) < period + 1:
        return None

    gains = []

    losses = []

    closes = [c.close for c in candles]

    for i in range(1, period + 1):

        change = closes[-period + i - 1] - closes[-period + i - 2]

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

    return 100 - (100 / (1 + rs))