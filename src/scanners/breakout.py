"""
Breakout Scanner
"""

from __future__ import annotations

from src.core.constants import SignalType, Strategy
from src.indicators import (
    highest_high,
    lowest_low,
    average_volume,
)
from src.models.signal import Signal


class BreakoutScanner:

    def scan(self, symbol: str, candles: list) -> list[Signal]:

        signals = []

        if len(candles) < 21:
            return signals

        latest = candles[-1]

        hh = highest_high(candles[:-1], 20)
        ll = lowest_low(candles[:-1], 20)
        avg_volume = average_volume(candles[:-1], 20)

        if hh is None or ll is None or avg_volume is None:
            return signals

        # BUY Breakout
        if (
            latest.close > hh
            and latest.volume > (avg_volume * 1.5)
        ):

            signals.append(
                Signal(
                    security_id=0,  # Temporary
                    strategy=Strategy.BREAKOUT,
                    signal_type=SignalType.BUY,
                    signal_price=latest.close,
                    current_ltp=latest.close,
                    confidence=85,
                    message="Price breakout with volume confirmation",
                    timestamp=latest.timestamp,
                )
            )

        # SELL Breakdown
        elif (
            latest.close < ll
            and latest.volume > (avg_volume * 1.5)
        ):

            signals.append(
                Signal(
                    security_id=0,  # Temporary
                    strategy=Strategy.BREAKOUT,
                    signal_type=SignalType.SELL,
                    signal_price=latest.close,
                    current_ltp=latest.close,
                    confidence=85,
                    message="Price breakdown with volume confirmation",
                    timestamp=latest.candle_time,
                )
            )

        return signals