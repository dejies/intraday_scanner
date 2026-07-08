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

    Primary Trend:
        EMA20 vs EMA50

    Confirmation:
        VWAP
        RSI
        Relative Volume

    Confidence is calculated from confirmations.
    """

    # ------------------------------------------------------------------

    def scan(
        self,
        symbol: str,
        candles: list[Candle],
        indicators: IndicatorData,
    ) -> list[Signal]:

        signals: list[Signal] = []

        #
        # Need EMA values.
        #
        if (
            indicators.ema20 is None
            or indicators.ema50 is None
        ):
            return signals

        latest = candles[-1]

        ema20 = indicators.ema20
        ema50 = indicators.ema50

        signal_type: SignalType | None = None

        #
        # Primary trend
        #
        if ema20 > ema50:
            signal_type = SignalType.BUY

        elif ema20 < ema50:
            signal_type = SignalType.SELL

        else:
            return signals

        confidence = self._calculate_confidence(
            signal_type,
            indicators,
        )

        message = self._build_message(
            signal_type,
            indicators,
        )

        signals.append(

            Signal(
                symbol=symbol,
                signal=signal_type,
                strategy=Strategy.TREND,
                price=indicators.ltp,
                confidence=confidence,
                timestamp=latest.timestamp,
                message=message,
            )
        )

        return signals

    # ------------------------------------------------------------------

    def _calculate_confidence(
        self,
        signal: SignalType,
        indicators: IndicatorData,
    ) -> int:
        """
        Calculate confidence score.
        """

        confidence = 40

        #
        # VWAP
        #
        if indicators.vwap is not None:

            if (
                signal == SignalType.BUY
                and indicators.ltp > indicators.vwap
            ):
                confidence += 20

            elif (
                signal == SignalType.SELL
                and indicators.ltp < indicators.vwap
            ):
                confidence += 20

        #
        # RSI
        #
        if indicators.rsi14 is not None:

            if signal == SignalType.BUY:

                if indicators.rsi14 >= 60:
                    confidence += 20

                elif indicators.rsi14 >= 50:
                    confidence += 10

            else:

                if indicators.rsi14 <= 40:
                    confidence += 20

                elif indicators.rsi14 <= 50:
                    confidence += 10

        #
        # Relative Volume
        #
        if indicators.relative_volume is not None:

            if indicators.relative_volume >= 2.0:
                confidence += 20

            elif indicators.relative_volume >= 1.0:
                confidence += 10

        #
        # Cap at 100%
        #
        return min(confidence, 100)

    # ------------------------------------------------------------------

    def _build_message(
        self,
        signal: SignalType,
        indicators: IndicatorData,
    ) -> str:
        """
        Build descriptive signal message.
        """

        trend = (
            "EMA20 > EMA50"
            if signal == SignalType.BUY
            else "EMA20 < EMA50"
        )

        parts = [trend]

        if indicators.vwap is not None:

            if signal == SignalType.BUY:

                parts.append(
                    "Above VWAP"
                    if indicators.ltp > indicators.vwap
                    else "Below VWAP"
                )

            else:

                parts.append(
                    "Below VWAP"
                    if indicators.ltp < indicators.vwap
                    else "Above VWAP"
                )

        if indicators.rsi14 is not None:
            parts.append(
                f"RSI={indicators.rsi14:.2f}"
            )

        if indicators.relative_volume is not None:
            parts.append(
                f"RVOL={indicators.relative_volume:.2f}"
            )

        return " | ".join(parts)