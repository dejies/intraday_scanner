"""
Supported candle intervals.
"""

from __future__ import annotations

from enum import Enum


class CandleInterval(str, Enum):
    ONE_MINUTE = "1m"
    THREE_MINUTE = "3m"
    FIVE_MINUTE = "5m"
    TEN_MINUTE = "10m"
    FIFTEEN_MINUTE = "15m"
    THIRTY_MINUTE = "30m"
    ONE_HOUR = "1h"
    ONE_DAY = "1d"