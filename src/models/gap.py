"""
Gap model.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum


class GapDirection(Enum):

    NONE = "NONE"
    UP = "UP"
    DOWN = "DOWN"


@dataclass(slots=True)
class Gap:

    #
    # Instrument
    #
    security_id: int

    #
    # Trading day
    #
    trading_day: date

    #
    # Previous day's closing price
    #
    previous_close: float

    #
    # Today's opening price
    #
    today_open: float

    #
    # Gap percentage
    #
    gap_percent: float

    #
    # Gap direction
    #
    direction: GapDirection

    #
    # Has the gap been filled?
    #
    gap_filled: bool = False

    #
    # Prevent duplicate BUY/SELL signals
    #
    buy_triggered: bool = False

    sell_triggered: bool = False