"""
Calculated technical indicators.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class IndicatorData:
    """
    Latest calculated technical indicators for a stock.

    This model stores only the latest indicator values.
    Indicator calculations are performed by the Indicator Engine.
    """

    # Live market price
    ltp: float

    # Trend
    ema9: float | None = None
    ema20: float | None = None
    ema50: float | None = None
    ema200: float | None = None

    # Momentum
    rsi14: float | None = None

    # MACD
    macd: float | None = None
    macd_signal: float | None = None
    macd_histogram: float | None = None

    # Trend Strength
    adx14: float | None = None

    # Intraday
    vwap: float | None = None

    # Volatility
    atr14: float | None = None

    # Volume
    average_volume20: float | None = None
    relative_volume: float | None = None

    # Runtime
    updated_at: datetime | None = None