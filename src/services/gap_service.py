"""
Maintains daily gap information.
"""

from __future__ import annotations

from datetime import time

from src.models import Candle, Gap, GapDirection
from src.repositories.candle_repository import CandleRepository
from datetime import date

class GapService:

    #
    # Minimum gap percentage
    #
    MIN_GAP_PERCENT = 1.0

    #
    # First completed candle
    #
    MARKET_OPEN = time(9, 15)

    def __init__(
            self,
            candle_repository: CandleRepository,
    ):

        self._repository = candle_repository

        self._gaps: dict[int, Gap] = {}
        self._current_day: date | None = None


    # ---------------------------------------------------------

    def process_candle(
        self,
        candle: Candle,
    ) -> None:

        trading_day = candle.candle_time.date()
        #
        # New trading day
        #
        if self._current_day != trading_day:
            self._current_day = trading_day
            self._gaps.clear()
        #
        # We calculate today's gap only once,
        # using the first completed 09:15 candle.
        #
        if candle.candle_time.time() != self.MARKET_OPEN:
            return

        security_id = int(candle.security_id)

        existing = self._gaps.get(security_id)

        if (
                existing is not None
                and existing.trading_day == trading_day
        ):
            return

        previous_close = self._repository.previous_day_close(
            security_id=candle.security_id,
            interval=candle.interval,
            trading_day=candle.candle_time.date(),
        )

        if previous_close <= 0:
            return

        today_open = float(candle.open)

        gap_percent = (
            (
                today_open - previous_close
            )
            / previous_close
        ) * 100.0

        if gap_percent >= self.MIN_GAP_PERCENT:

            direction = GapDirection.UP

        elif gap_percent <= -self.MIN_GAP_PERCENT:

            direction = GapDirection.DOWN

        else:

            direction = GapDirection.NONE

        self._gaps[security_id] = Gap(
            security_id=security_id,
            trading_day=candle.candle_time.date(),
            previous_close=previous_close,
            today_open=today_open,
            gap_percent=gap_percent,
            direction=direction,
        )

    # ---------------------------------------------------------

    def get(
        self,
        security_id: int,
    ) -> Gap | None:

        return self._gaps.get(
            security_id,
        )

    # ---------------------------------------------------------

    def clear(self) -> None:

        self._gaps.clear()

    # ---------------------------------------------------------

