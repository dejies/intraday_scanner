"""
Builds OHLC candles from MarketData ticks.
"""

from __future__ import annotations

from datetime import datetime, timezone
from threading import RLock
from src.models import CandleBuilderResult
from src.models.tick import Tick

from src.models import (
    Candle,
    CandleBuilderState,
    CandleInterval,
)


class CandleBuilder:

    def __init__(self):

        self._states: dict[str, CandleBuilderState] = {}

        self._lock = RLock()

    # ----------------------------------------------------------

    def process_tick(
            self,
            tick: Tick,
    ) -> CandleBuilderResult:
        """
        Processes a market tick and returns the current candle along with any
        completed candles.
        """

        with self._lock:

            security_id = tick.security_id

            state = self._states.get(security_id)

            tick_time = self._minute_start(
                tick.timestamp
            )

            # ------------------------------------------------------
            # First tick for this instrument
            # ------------------------------------------------------

            if state is None:
                candle = self._new_candle(
                    tick,
                    tick_time,
                )

                self._states[security_id] = CandleBuilderState(
                    candle=candle,
                    last_traded_volume=tick.volume,
                )

                return CandleBuilderResult(
                    current_candle=candle,
                    completed_candles=[],
                )

            current = state.candle

            # ------------------------------------------------------
            # Same candle
            # ------------------------------------------------------

            if current.candle_time == tick_time:
                self._update_candle(
                    state,
                    tick,
                )

                return CandleBuilderResult(
                    current_candle=state.candle,
                    completed_candles=[],
                )

            # ------------------------------------------------------
            # New candle
            # ------------------------------------------------------

            completed = current
            completed.is_closed = True

            candle = self._new_candle(
                tick,
                tick_time,
            )

            self._states[security_id] = CandleBuilderState(
                candle=candle,
                last_traded_volume=tick.volume,
            )

            return CandleBuilderResult(
                current_candle=candle,
                completed_candles=[completed],
            )

    # ----------------------------------------------------------

    def current_candle(
        self,
        security_id: str,
    ) -> Candle | None:

        with self._lock:

            state = self._states.get(security_id)

            return None if state is None else state.candle

    # ----------------------------------------------------------

    def _update_candle(
            self,
            state: CandleBuilderState,
            tick: Tick,
    ) -> None:

        candle = state.candle

        price = tick.ltp

        candle.high = max(
            candle.high,
            price,
        )

        candle.low = min(
            candle.low,
            price,
        )

        candle.close = price

        delta = max(
            0,
            tick.volume - state.last_traded_volume,
        )

        candle.volume += delta

        state.last_traded_volume = tick.volume

    # ----------------------------------------------------------

    def _new_candle(
            self,
            tick: Tick,
            candle_time: datetime,
    ) -> Candle:

        price = tick.ltp

        return Candle(
            security_id=tick.security_id,
            interval=CandleInterval.ONE_MINUTE,
            candle_time=candle_time,
            open=price,
            high=price,
            low=price,
            close=price,
            volume=0,
        )

    def reset(self) -> None:
        with self._lock:
            self._states.clear()

    def remove_security(
            self,
            security_id: str,
    ) -> None:
        with self._lock:
            self._states.pop(security_id, None)
    # ----------------------------------------------------------

    @staticmethod
    def _minute_start(
        dt: datetime,
    ) -> datetime:

        return dt.replace(
            second=0,
            microsecond=0,
        )