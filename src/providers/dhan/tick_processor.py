"""
Converts Dhan WebSocket messages into internal Tick objects.
"""

from __future__ import annotations

from datetime import datetime

from src.models.tick import Tick
from src.services.watchlist import WatchlistService
from decimal import Decimal

class TickProcessor:
    """
    Converts raw Dhan WebSocket messages into Tick models.
    """

    def __init__(
            self,
            watchlist: WatchlistService,
    ) -> None:

        self._watchlist = watchlist

    def process(
            self,
            message: dict,
    ) -> Tick | None:
        """
        Convert a Dhan WebSocket message into a Tick.

        Returns None for unsupported messages.
        """

        if not isinstance(message, dict):
            return None

        if message.get("type") != "Full Data":
            return None

        security_id = int(
            message["security_id"]
        )

        instrument = (
            self._watchlist.get_instrument_by_security_id(
                security_id
            )
        )

        if instrument is None:
            return None

        trade_time = datetime.strptime(
            message["LTT"],
            "%H:%M:%S",
        )

        now = datetime.now()

        trade_time = trade_time.replace(
            year=now.year,
            month=now.month,
            day=now.day,
        )

        return Tick(
            security_id=security_id,
            timestamp=trade_time,
            ltp=Decimal(str(message["LTP"])),
            volume=int(message["volume"]),
        )