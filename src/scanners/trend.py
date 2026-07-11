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

from src.core.config import settings

class TrendScanner:

    def __init__(self):
        self.settings = settings
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

        assert signal_type is not None
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
                security_id=0,  # Temporary
                strategy=Strategy.TREND,
                signal_type=signal_type,
                signal_price=indicators.ltp,
                current_ltp=indicators.ltp,
                confidence=confidence,
                message=message,
                timestamp=latest.candle_time,
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

        Maximum Score = 100

        Trend      : 30
        VWAP       : 20
        RSI        : 20
        RVOL       : 15
        EMA Gap    : 15
        """

        confidence = 0

        #
        # ----------------------------------------------------------
        # EMA Trend
        # ----------------------------------------------------------
        #
        confidence += self.settings.confidence_ema_weight

        #
        # ----------------------------------------------------------
        # VWAP
        # ----------------------------------------------------------
        #
        if indicators.vwap is not None:

            if signal == SignalType.BUY:

                if indicators.ltp > indicators.vwap:

                    confidence += (
                        self.settings.confidence_vwap_weight
                    )

                elif abs(
                        indicators.ltp - indicators.vwap
                ) < (
                        indicators.vwap * 0.001
                ):

                    confidence += (
                            self.settings.confidence_vwap_weight // 2
                    )

            else:

                if indicators.ltp < indicators.vwap:

                    confidence += (
                        self.settings.confidence_vwap_weight
                    )

                elif abs(
                        indicators.ltp - indicators.vwap
                ) < (
                        indicators.vwap * 0.001
                ):

                    confidence += (
                            self.settings.confidence_vwap_weight // 2
                    )

        #
        # ----------------------------------------------------------
        # RSI
        # ----------------------------------------------------------
        #
        if indicators.rsi14 is not None:

            rsi = indicators.rsi14

            if signal == SignalType.BUY:

                if rsi >= self.settings.rsi_buy_strong:

                    confidence += (
                        self.settings.confidence_rsi_weight
                    )

                elif rsi >= self.settings.rsi_buy_medium:

                    confidence += (
                        int(
                            self.settings.confidence_rsi_weight
                            * 0.75
                        )
                    )

                elif rsi >= self.settings.rsi_buy_weak:

                    confidence += (
                        int(
                            self.settings.confidence_rsi_weight
                            * 0.50
                        )
                    )

                elif rsi >= self.settings.rsi_buy_min:

                    confidence += (
                        int(
                            self.settings.confidence_rsi_weight
                            * 0.25
                        )
                    )

            else:

                if rsi <= self.settings.rsi_sell_strong:

                    confidence += (
                        self.settings.confidence_rsi_weight
                    )

                elif rsi <= self.settings.rsi_sell_medium:

                    confidence += (
                        int(
                            self.settings.confidence_rsi_weight
                            * 0.75
                        )
                    )

                elif rsi <= self.settings.rsi_sell_weak:

                    confidence += (
                        int(
                            self.settings.confidence_rsi_weight
                            * 0.50
                        )
                    )

                elif rsi <= self.settings.rsi_sell_max:

                    confidence += (
                        int(
                            self.settings.confidence_rsi_weight
                            * 0.25
                        )
                    )

        #
        # ----------------------------------------------------------
        # Relative Volume
        # ----------------------------------------------------------
        #
        if indicators.relative_volume is not None:

            rvol = indicators.relative_volume

            if rvol >= self.settings.rvol_high:

                confidence += (
                    self.settings.confidence_rvol_weight
                )

            elif rvol >= self.settings.rvol_medium:

                confidence += (
                    int(
                        self.settings.confidence_rvol_weight
                        * 0.80
                    )
                )

            elif rvol >= self.settings.rvol_normal:

                confidence += (
                    int(
                        self.settings.confidence_rvol_weight
                        * 0.60
                    )
                )

            elif rvol >= self.settings.rvol_low:

                confidence += (
                    int(
                        self.settings.confidence_rvol_weight
                        * 0.30
                    )
                )

        #
        # ----------------------------------------------------------
        # EMA Gap
        # ----------------------------------------------------------
        #
        if (
                indicators.ema20 is not None
                and indicators.ema50 is not None
                and indicators.ema50 != 0
        ):

            gap = (
                          abs(
                              indicators.ema20
                              - indicators.ema50
                          )
                          / indicators.ema50
                  ) * 100

            if gap >= self.settings.ema_gap_strong:

                confidence += (
                    self.settings.confidence_ema_gap_weight
                )

            elif gap >= self.settings.ema_gap_medium:

                confidence += (
                    int(
                        self.settings.confidence_ema_gap_weight
                        * 0.80
                    )
                )

            elif gap >= self.settings.ema_gap_normal:

                confidence += (
                    int(
                        self.settings.confidence_ema_gap_weight
                        * 0.60
                    )
                )

            elif gap >= self.settings.ema_gap_weak:

                confidence += (
                    int(
                        self.settings.confidence_ema_gap_weight
                        * 0.40
                    )
                )

            elif gap >= self.settings.ema_gap_min:

                confidence += (
                    int(
                        self.settings.confidence_ema_gap_weight
                        * 0.20
                    )
                )

        #
        # Clamp to 100%
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