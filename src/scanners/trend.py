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

    BUY:
        EMA20 > EMA50
        Price > VWAP
        RSI > 55

    SELL:
        EMA20 < EMA50
        Price < VWAP
        RSI < 45
    """

    def scan(
            self,
            symbol: str,
            candles: list[Candle],
            indicators: IndicatorData,
    ) -> list[Signal]:

        signals: list[Signal] = []

        #
        # Need all indicators.
        #
        if (
            indicators.ema20 is None
            or indicators.ema50 is None
            or indicators.vwap is None
            or indicators.rsi14 is None
        ):
            return signals

        latest = candles[-1]

        ema20 = indicators.ema20
        ema50 = indicators.ema50

        price = indicators.ltp
        vwap = indicators.vwap
        rsi = indicators.rsi14

        #
        # BUY
        #
        if (
            ema20 > ema50
            and price > vwap
            and rsi > 55
        ):

            signals.append(

                Signal(
                    symbol=symbol,
                    signal=SignalType.BUY,
                    strategy=Strategy.TREND,
                    price=price,
                    confidence=80,
                    timestamp=latest.timestamp,
                    message=(
                        f"EMA20 > EMA50 | "
                        f"Price > VWAP | "
                        f"RSI={rsi:.2f}"
                    ),
                )
            )

        #
        # SELL
        #
        elif (
            ema20 < ema50
            and price < vwap
            and rsi < 45
        ):

            signals.append(

                Signal(
                    symbol=symbol,
                    signal=SignalType.SELL,
                    strategy=Strategy.TREND,
                    price=price,
                    confidence=80,
                    timestamp=latest.timestamp,
                    message=(
                        f"EMA20 < EMA50 | "
                        f"Price < VWAP | "
                        f"RSI={rsi:.2f}"
                    ),
                )
            )

        return signals