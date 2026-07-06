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

        if len(candles) < 20:
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
                    symbol=symbol,
                    strategy=Strategy.BREAKOUT,
                    signal=SignalType.BUY,
                    price=latest.close,
                    confidence=85,
                    timestamp=latest.timestamp,
                    message="Price breakout with volume confirmation",
                )
            )

        # SELL Breakdown
        elif (
            latest.close < ll
            and latest.volume > (avg_volume * 1.5)
        ):

            signals.append(
                Signal(
                    symbol=symbol,
                    strategy=Strategy.BREAKOUT,
                    signal=SignalType.SELL,
                    price=latest.close,
                    confidence=85,
                    timestamp=latest.timestamp,
                    message="Price breakdown with volume confirmation",
                )
            )

        return signals