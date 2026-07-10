"""
Application market status model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from src.models.enums import ConnectionState, MarketState, ScannerState


@dataclass(slots=True)
class MarketStatus:
    """
    Represents the overall runtime status of the application.
    """

    # Market
    market_state: MarketState = MarketState.CLOSED

    # WebSocket
    connection_state: ConnectionState = ConnectionState.DISCONNECTED

    # Scanner
    scanner_state: ScannerState = ScannerState.IDLE

    # Runtime statistics
    watching_count: int = 0

    # Timestamps
    application_started_at: datetime = field(default_factory=datetime.now)

    last_tick_at: Optional[datetime] = None

    last_scan_at: Optional[datetime] = None

    last_dashboard_refresh_at: Optional[datetime] = None