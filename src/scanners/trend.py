"""
Trend Scanner

Generates BUY/SELL signals using the shared
Indicator Engine.
"""

from __future__ import annotations

from src.models.candle import Candle
from src.models.indicator import IndicatorData
from src.models.signal import Signal

from src.core.constants import SignalType
from src.core.constants import Strategy


class TrendScanner:
    """
    Trend-based scanner.

    Uses EMA20 and EMA50 from the shared
    Indicator Engine.
    """

    def scan(
            self,
            symbol: str,
            candles: list[Candle],
            indicators: IndicatorData,
    ) -> list[Signal]:
        """
        Scan one symbol for trend signals.
        """

        signals: list[Signal] = []

        #
        # Need EMA values.
        #
        if (
                indicators.ema20 is None
                or indicators.ema50 is None
        ):
            return signals

        ema20 = indicators.ema20
        ema50 = indicators.ema50

        price = indicators.ltp

        #
        # BUY
        #
        if ema20 > ema50:

            signals.append(

                Signal(
                    symbol=symbol,
                    signal=SignalType.BUY,
                    strategy=Strategy.TREND,
                    price=price,
                    confidence=80,
                    timestamp=candles[-1].timestamp,
                    message=(
                        f"EMA20 ({ema20:.2f}) "
                        f"> EMA50 ({ema50:.2f})"
                    ),
                )
            )

        #
        # SELL
        #
        elif ema20 < ema50:

            signals.append(

                Signal(
                    symbol=symbol,
                    signal=SignalType.SELL,
                    strategy=Strategy.TREND,
                    price=price,
                    confidence=80,
                    timestamp=candles[-1].timestamp,
                    message=(
                        f"EMA20 ({ema20:.2f}) "
                        f"< EMA50 ({ema50:.2f})"
                    ),
                )
            )

        return signals