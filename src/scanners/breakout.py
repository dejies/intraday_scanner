"""
Breakout Scanner
"""

from __future__ import annotations

from src.core.constants import SignalType, Strategy
from src.models.candle import Candle
from src.models.signal import Signal


class BreakoutScanner:

    @staticmethod
    def _highest_high(
        candles: list[Candle],
        period: int,
    ):

        if len(candles) < period:
            return None

        return max(
            candle.high
            for candle in candles[-period:]
        )

    @staticmethod
    def _lowest_low(
        candles: list[Candle],
        period: int,
    ):

        if len(candles) < period:
            return None

        return min(
            candle.low
            for candle in candles[-period:]
        )

    @staticmethod
    def _average_volume(
        candles: list[Candle],
        period: int,
    ):

        if len(candles) < period:
            return None

        return (
            sum(
                candle.volume
                for candle in candles[-period:]
            )
            / period
        )

    # ------------------------------------------------------------------

    def scan(
        self,
        symbol: str,
        candles: list[Candle],
    ) -> list[Signal]:

        signals: list[Signal] = []

        if len(candles) < 21:
            return signals

        latest = candles[-1]

        hh = self._highest_high(
            candles[:-1],
            20,
        )

        ll = self._lowest_low(
            candles[:-1],
            20,
        )

        avg_volume = self._average_volume(
            candles[:-1],
            20,
        )

        if (
            hh is None
            or ll is None
            or avg_volume is None
        ):
            return signals

        #
        # BUY Breakout
        #
        if (
            latest.close > hh
            and latest.volume > (avg_volume * 1.5)
        ):

            signals.append(
                Signal(
                    security_id=0,
                    strategy=Strategy.BREAKOUT,
                    signal_type=SignalType.BUY,
                    signal_price=latest.close,
                    current_ltp=latest.close,
                    confidence=85,
                    message="Price breakout with volume confirmation",
                    timestamp=latest.candle_time,
                )
            )

        #
        # SELL Breakdown
        #
        elif (
            latest.close < ll
            and latest.volume > (avg_volume * 1.5)
        ):

            signals.append(
                Signal(
                    security_id=0,
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