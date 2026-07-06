"""
Trend Scanner

Detects bullish and bearish trend setups.
"""

from __future__ import annotations

from src.core.constants import SignalType, Strategy
from src.indicators import ema, rsi, vwap
from src.models.signal import Signal


class TrendScanner:

    def scan(
        self,
        symbol: str,
        candles: list,
    ) -> list[Signal]:

        signals = []

        if len(candles) < 50:
            return signals

        ema20 = ema(candles, 20)
        ema50 = ema(candles, 50)
        rsi14 = rsi(candles)
        current_vwap = vwap(candles)

        latest = candles[-1]

        if None in (ema20, ema50, rsi14, current_vwap):
            return signals

        # ---------------------------------------------------------
        # BUY
        # ---------------------------------------------------------

        if (
            ema20 > ema50
            and latest.close > current_vwap
            and rsi14 > 55
        ):

            signals.append(
                Signal(
                    symbol=symbol,
                    strategy=Strategy.TREND,
                    signal=SignalType.BUY,
                    price=latest.close,
                    confidence=80,
                    timestamp=latest.timestamp,
                    message=(
                        "EMA20 > EMA50, "
                        "Price above VWAP, "
                        "RSI > 55"
                    ),
                )
            )

        # ---------------------------------------------------------
        # SELL
        # ---------------------------------------------------------

        elif (
            ema20 < ema50
            and latest.close < current_vwap
            and rsi14 < 45
        ):

            signals.append(
                Signal(
                    symbol=symbol,
                    strategy=Strategy.TREND,
                    signal=SignalType.SELL,
                    price=latest.close,
                    confidence=80,
                    timestamp=latest.timestamp,
                    message=(
                        "EMA20 < EMA50, "
                        "Price below VWAP, "
                        "RSI < 45"
                    ),
                )
            )

        return signals