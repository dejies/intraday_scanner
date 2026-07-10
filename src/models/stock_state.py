"""
Runtime state of a stock.

This is the central model used by the MarketDataStore.
Each instrument being monitored has exactly one StockState instance.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from src.models.indicator import IndicatorData
from src.models.candle import Candle
from src.models.instrument import Instrument
from src.models.signal import Signal
from src.models.tick import Tick


@dataclass(slots=True)
class StockState:
    """
    Represents the complete runtime state of a stock.

    This class aggregates all live information required by the scanner,
    dashboard and alert modules.
    """

    # Static instrument information
    instrument: Instrument

    # Latest market tick
    tick: Optional[Tick] = None

    # Current (building) candle
    current_candle: Optional[Candle] = None

    # Latest calculated indicators
    indicator: Optional[IndicatorData] = None

    # Current active BUY/SELL signal
    active_signal: Optional[Signal] = None

    # Runtime information
    last_updated: datetime = field(default_factory=datetime.now)

    # Whether this stock is currently enabled for scanning
    enabled: bool = True