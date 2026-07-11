"""
Persistent indicator record.

Represents a single calculated indicator value
stored in SQLite.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class IndicatorType(str, Enum):
    """
    Supported indicator types.
    """

    EMA_9 = "EMA_9"
    EMA_20 = "EMA_20"
    EMA_50 = "EMA_50"
    EMA_200 = "EMA_200"

    RSI_14 = "RSI_14"

    MACD = "MACD"
    MACD_SIGNAL = "MACD_SIGNAL"
    MACD_HISTOGRAM = "MACD_HISTOGRAM"

    ADX_14 = "ADX_14"

    VWAP = "VWAP"


@dataclass(slots=True)
class IndicatorRecord:
    """
    One calculated indicator value.

    Example:

        RELIANCE
        1m
        EMA20
        09:31
        1468.25
    """

    security_id: str

    timeframe: str

    indicator: IndicatorType

    candle_time: datetime

    value: float