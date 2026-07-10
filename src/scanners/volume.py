"""
Volume Scanner

Detects unusual volume with price confirmation.
"""

from __future__ import annotations

from src.core.constants import SignalType, Strategy
from src.indicators import average_volume
from src.models.candle import Candle
from src.models.signal import Signal


class VolumeScanner:

    def scan(
        self,
        symbol: str,
        candles: list[Candle],
    ) -> list[Signal]:

        signals = []

        if len(candles) < 21:
            return signals

        latest = candles[-1]
        previous = candles[-2]

        avg_volume = average_volume(candles[:-1], 20)

        if avg_volume is None:
            return signals

        # BUY
        if (
            latest.volume >= avg_volume * 2
            and latest.close > latest.open
            and latest.close > previous.close
        ):

            signals.append(
                Signal(
                    security_id=0,  # Temporary
                    strategy=Strategy.VOLUME,
                    signal_type=SignalType.BUY,
                    signal_price=latest.close,
                    current_ltp=latest.close,
                    confidence=75,
                    message="Bullish volume spike",
                    timestamp=latest.timestamp,
                )
            )

        # SELL
        elif (
            latest.volume >= avg_volume * 2
            and latest.close < latest.open
            and latest.close < previous.close
        ):

            signals.append(
                Signal(
                    security_id=0,  # Temporary
                    strategy=Strategy.VOLUME,
                    signal_type=SignalType.SELL,
                    signal_price=latest.close,
                    current_ltp=latest.close,
                    confidence=75,
                    message="Bearish volume spike",
                    timestamp=latest.timestamp,
                )
            )

        return signals