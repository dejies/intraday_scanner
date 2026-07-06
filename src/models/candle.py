"""
Market candle model.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Candle:
    """
    Represents a single OHLCV candle.
    """

    timestamp: datetime

    open: float
    high: float
    low: float
    close: float

    volume: int