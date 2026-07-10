"""
Market candle model.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from src.models.enums import TimeFrame


@dataclass(slots=True)
class Candle:
    """
    Represents a single OHLCV candle.

    This model is timeframe-agnostic and can represent
    1-minute, 5-minute, 15-minute, hourly or daily candles.
    """

    timestamp: datetime

    timeframe: TimeFrame = TimeFrame.ONE_MINUTE

    open: Decimal = Decimal("0")

    high: Decimal = Decimal("0")

    low: Decimal = Decimal("0")

    close: Decimal = Decimal("0")

    volume: int = 0

    is_closed: bool = False