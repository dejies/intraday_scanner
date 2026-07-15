"""
Maintains Opening Range (ORB) for all instruments.
"""

from __future__ import annotations

from datetime import time

from src.models import Candle, OpeningRange


class OpeningRangeService:

    #
    # ORB window
    #
    START_TIME = time(9, 15)
    END_TIME = time(9, 20)

    def __init__(self):

        self._ranges: dict[int, OpeningRange] = {}

    # ---------------------------------------------------------

    def process_candle(
        self,
        candle: Candle,
    ) -> None:

        security_id = int(candle.security_id)

        trading_day = candle.candle_time.date()

        orb = self._ranges.get(
            security_id
        )

        if (
            orb is None
            or orb.trading_day != trading_day
        ):

            orb = OpeningRange(
                security_id=security_id,
                trading_day=trading_day,
                high=candle.high,
                low=candle.low,
            )

            self._ranges[security_id] = orb

        candle_time = candle.candle_time.time()

        #
        # Ignore candles before market open
        #
        if candle_time < self.START_TIME:
            return

        #
        # Update opening range
        #
        if (
            not orb.locked
            and candle_time < self.END_TIME
        ):

            orb.high = max(
                orb.high,
                candle.high,
            )

            orb.low = min(
                orb.low,
                candle.low,
            )

            return

        #
        # Lock after ORB window
        #
        if (
            not orb.locked
            and candle_time >= self.END_TIME
        ):

            orb.locked = True

    # ---------------------------------------------------------

    def get(
        self,
        security_id: int,
    ) -> OpeningRange | None:

        return self._ranges.get(
            security_id
        )

    # ---------------------------------------------------------

    def clear(self) -> None:

        self._ranges.clear()