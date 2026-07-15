"""
Opening Range model.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(slots=True)
class OpeningRange:

    security_id: int

    trading_day: date

    high: float

    low: float

    locked: bool = False

    #
    # Prevent duplicate ORB signals
    #
    buy_triggered: bool = False

    sell_triggered: bool = False