from __future__ import annotations

from src.models.indicator import IndicatorData
from src.models.technical_confidence_result import (
    TechnicalConfidenceResult,
)


class TechnicalConfidenceEngine:
    """
    Calculates a technical confidence score from IndicatorData.

    Score range:
        0 - 100

    The engine evaluates:
        - EMA trend alignment
        - RSI momentum
        - MACD
        - ADX
        - VWAP
        - RVOL
        - Volume Spike
        - Gap Strength
        - ATR quality

    Volume and volatility indicators strengthen an existing
    directional setup. They do not independently create a
    BUY or SELL signal.
    """

    MAX_RAW_SCORE = 90.0

    # ------------------------------------------------------------------
    # Component maximum scores
    # ------------------------------------------------------------------

    MAX_TREND_SCORE = 15.0
    MAX_MOMENTUM_SCORE = 10.0
    MAX_MACD_SCORE = 10.0
    MAX_ADX_SCORE = 10.0
    MAX_VWAP_SCORE = 10.0
    MAX_RVOL_SCORE = 10.0
    MAX_VOLUME_SPIKE_SCORE = 10.0
    MAX_GAP_SCORE = 10.0
    MAX_ATR_SCORE = 5.0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @classmethod
    def calculate(
        cls,
        indicator: IndicatorData | None,
    ) -> TechnicalConfidenceResult | None:
        """
        Calculate technical confidence.

        Parameters
        ----------
        indicator:
            Latest IndicatorData for the stock.

        Returns
        -------
        TechnicalConfidenceResult | None
        """

        if indicator is None:
            return None

        #
        # Directional scores.
        #
        buy_score = 0.0
        sell_score = 0.0

        #
        # Individual component scores.
        #
        trend_score = 0.0
        momentum_score = 0.0
        macd_score = 0.0
        adx_score = 0.0
        vwap_score = 0.0
        rvol_score = 0.0
        volume_spike_score = 0.0
        gap_score = 0.0
        atr_score = 0.0

        # ==============================================================
        # TREND — EMA
        # ==============================================================

        trend_direction, trend_score = cls._trend_score(
            indicator
        )

        if trend_direction == "BUY":
            buy_score += trend_score

        elif trend_direction == "SELL":
            sell_score += trend_score

        # ==============================================================
        # MOMENTUM — RSI
        # ==============================================================

        momentum_direction, momentum_score = (
            cls._momentum_score(indicator)
        )

        if momentum_direction == "BUY":
            buy_score += momentum_score

        elif momentum_direction == "SELL":
            sell_score += momentum_score

        # ==============================================================
        # MACD
        # ==============================================================

        macd_direction, macd_score = cls._macd_score(
            indicator
        )

        if macd_direction == "BUY":
            buy_score += macd_score

        elif macd_direction == "SELL":
            sell_score += macd_score

        # ==============================================================
        # ADX — TREND STRENGTH
        # ==============================================================

        adx_score = cls._adx_score(indicator)

        #
        # ADX has no direction.
        # It will strengthen whichever side is currently leading.
        #

        # ==============================================================
        # VWAP
        # ==============================================================

        vwap_direction, vwap_score = cls._vwap_score(
            indicator
        )

        if vwap_direction == "BUY":
            buy_score += vwap_score

        elif vwap_direction == "SELL":
            sell_score += vwap_score

        # ==============================================================
        # RVOL
        # ==============================================================

        rvol_score = cls._rvol_score(indicator)

        #
        # RVOL has no direction.
        # Apply it after determining the directional leader.
        #

        # ==============================================================
        # VOLUME SPIKE
        # ==============================================================

        volume_spike_score = cls._volume_spike_score(
            indicator
        )

        #
        # Volume spike has no direction.
        # Apply it after determining the directional leader.
        #

        # ==============================================================
        # GAP STRENGTH
        # ==============================================================

        gap_direction, gap_score = cls._gap_score(
            indicator
        )

        if gap_direction == "BUY":
            buy_score += gap_score

        elif gap_direction == "SELL":
            sell_score += gap_score

        # ==============================================================
        # Determine current directional leader
        # ==============================================================

        if buy_score > sell_score:
            signal = "BUY"

        elif sell_score > buy_score:
            signal = "SELL"

        else:
            signal = "NEUTRAL"

        # ==============================================================
        # ADX / RVOL / Volume Spike / ATR
        #
        # These are confirmation factors rather than standalone
        # directional indicators.
        # ==============================================================

        confirmation_score = (
            adx_score
            + rvol_score
            + volume_spike_score
            + atr_score
        )

        if signal == "BUY":

            buy_score += confirmation_score

        elif signal == "SELL":

            sell_score += confirmation_score

        # ==============================================================
        # ATR quality
        # ==============================================================

        #
        # ATR was calculated above as part of the confirmation score.
        #
        atr_score = cls._atr_score(indicator)

        #
        # Recalculate confirmation with the actual ATR score.
        #
        confirmation_score = (
            adx_score
            + rvol_score
            + volume_spike_score
            + atr_score
        )

        #
        # The previous confirmation allocation needs to be corrected
        # because ATR is calculated after the initial directional
        # comparison.
        #
        #
        # Rebuild the directional totals from scratch.
        #

        buy_score = 0.0
        sell_score = 0.0

        if trend_direction == "BUY":
            buy_score += trend_score

        elif trend_direction == "SELL":
            sell_score += trend_score

        if momentum_direction == "BUY":
            buy_score += momentum_score

        elif momentum_direction == "SELL":
            sell_score += momentum_score

        if macd_direction == "BUY":
            buy_score += macd_score

        elif macd_direction == "SELL":
            sell_score += macd_score

        if vwap_direction == "BUY":
            buy_score += vwap_score

        elif vwap_direction == "SELL":
            sell_score += vwap_score

        if gap_direction == "BUY":
            buy_score += gap_score

        elif gap_direction == "SELL":
            sell_score += gap_score

        #
        # Determine leader before applying neutral confirmation factors.
        #

        if buy_score > sell_score:
            signal = "BUY"

        elif sell_score > buy_score:
            signal = "SELL"

        else:
            signal = "NEUTRAL"

        #
        # Confirmation factors strengthen the current leader.
        #

        if signal == "BUY":
            buy_score += confirmation_score

        elif signal == "SELL":
            sell_score += confirmation_score

        #
        # Raw technical score.
        #

        raw_score = max(
            buy_score,
            sell_score,
        )

        #
        # Normalize 0-90 into 0-100.
        #

        score = min(
            100.0,
            round(
                (raw_score / cls.MAX_RAW_SCORE) * 100,
                2,
            ),
        )

        #
        # Do not call a weak directional difference a strong signal.
        #

        if signal != "NEUTRAL":

            directional_difference = abs(
                buy_score - sell_score
            )

            if directional_difference < 5:
                signal = "NEUTRAL"
                score = min(
                    score,
                    49.0,
                )

        confidence = cls._confidence_level(
            score
        )

        return TechnicalConfidenceResult(
            score=score,
            signal=signal,
            confidence=confidence,

            trend_score=trend_score,
            momentum_score=momentum_score,
            macd_score=macd_score,
            adx_score=adx_score,
            vwap_score=vwap_score,
            rvol_score=rvol_score,
            volume_spike_score=volume_spike_score,
            gap_score=gap_score,
            atr_score=atr_score,
        )

    # ------------------------------------------------------------------
    # EMA Trend
    # ------------------------------------------------------------------

    @classmethod
    def _trend_score(
        cls,
        indicator: IndicatorData,
    ) -> tuple[str, float]:

        ema9 = indicator.ema9
        ema20 = indicator.ema20
        ema50 = indicator.ema50
        ema200 = indicator.ema200

        if any(
            value is None
            for value in (
                ema9,
                ema20,
                ema50,
                ema200,
            )
        ):
            return "NEUTRAL", 0.0

        #
        # Strong bullish alignment
        #
        if (
            ema9 > ema20
            and ema20 > ema50
            and ema50 > ema200
        ):
            return "BUY", 15.0

        #
        # Partial bullish alignment
        #
        if (
            ema9 > ema20
            and ema20 > ema50
        ):
            return "BUY", 10.0

        #
        # Weak bullish alignment
        #
        if ema9 > ema20:
            return "BUY", 6.0

        #
        # Strong bearish alignment
        #
        if (
            ema9 < ema20
            and ema20 < ema50
            and ema50 < ema200
        ):
            return "SELL", 15.0

        #
        # Partial bearish alignment
        #
        if (
            ema9 < ema20
            and ema20 < ema50
        ):
            return "SELL", 10.0

        #
        # Weak bearish alignment
        #
        if ema9 < ema20:
            return "SELL", 6.0

        return "NEUTRAL", 0.0

    # ------------------------------------------------------------------
    # RSI
    # ------------------------------------------------------------------

    @classmethod
    def _momentum_score(
            cls,
            indicator: IndicatorData,
    ) -> tuple[str, float]:

        rsi = indicator.rsi14

        if rsi is None:
            return "NEUTRAL", 0.0

        #
        # Strong bullish momentum
        #
        if 55 <= rsi < 70:
            return "BUY", 10.0

        #
        # Moderate bullish momentum
        #
        if 50 < rsi < 55:
            return "BUY", 6.0

        #
        # Overbought - reduced bullish confirmation
        #
        if 70 <= rsi < 80:
            return "BUY", 5.0

        #
        # Strong bearish momentum
        #
        if 30 < rsi <= 45:
            return "SELL", 10.0

        #
        # Moderate bearish momentum
        #
        if 45 < rsi < 50:
            return "SELL", 6.0

        #
        # Oversold - reduced bearish confirmation
        #
        if 20 < rsi <= 30:
            return "SELL", 5.0

        #
        # RSI 50 is neutral.
        #
        return "NEUTRAL", 0.0
    # ------------------------------------------------------------------
    # MACD
    # ------------------------------------------------------------------

    @classmethod
    def _macd_score(
        cls,
        indicator: IndicatorData,
    ) -> tuple[str, float]:

        macd = indicator.macd
        signal = indicator.macd_signal
        histogram = indicator.macd_histogram

        if (
            macd is None
            or signal is None
            or histogram is None
        ):
            return "NEUTRAL", 0.0

        if (
            macd > signal
            and histogram > 0
        ):
            return "BUY", 10.0

        if (
            macd < signal
            and histogram < 0
        ):
            return "SELL", 10.0

        if macd > signal:
            return "BUY", 5.0

        if macd < signal:
            return "SELL", 5.0

        return "NEUTRAL", 0.0

    # ------------------------------------------------------------------
    # ADX
    # ------------------------------------------------------------------

    @classmethod
    def _adx_score(
        cls,
        indicator: IndicatorData,
    ) -> float:

        adx = indicator.adx14

        if adx is None:
            return 0.0

        if adx >= 30:
            return 10.0

        if adx >= 25:
            return 8.0

        if adx >= 20:
            return 5.0

        return 2.0

    # ------------------------------------------------------------------
    # VWAP
    # ------------------------------------------------------------------

    @classmethod
    def _vwap_score(
        cls,
        indicator: IndicatorData,
    ) -> tuple[str, float]:

        ltp = indicator.ltp
        vwap = indicator.vwap

        if ltp is None or vwap is None:
            return "NEUTRAL", 0.0

        if ltp > vwap:
            return "BUY", 10.0

        if ltp < vwap:
            return "SELL", 10.0

        return "NEUTRAL", 0.0

    # ------------------------------------------------------------------
    # RVOL
    # ------------------------------------------------------------------

    @classmethod
    def _rvol_score(
        cls,
        indicator: IndicatorData,
    ) -> float:

        rvol = indicator.relative_volume

        if rvol is None:
            return 0.0

        if rvol >= 3.0:
            return 10.0

        if rvol >= 2.0:
            return 8.0

        if rvol >= 1.5:
            return 6.0

        if rvol >= 1.0:
            return 3.0

        return 0.0

    # ------------------------------------------------------------------
    # Volume Spike
    # ------------------------------------------------------------------

    @classmethod
    def _volume_spike_score(
        cls,
        indicator: IndicatorData,
    ) -> float:

        if not indicator.has_volume_spike:
            return 0.0

        score = indicator.volume_spike_score

        if score is None:
            return 0.0

        return min(
            cls.MAX_VOLUME_SPIKE_SCORE,
            max(0.0, float(score)),
        )

    # ------------------------------------------------------------------
    # Gap Strength
    # ------------------------------------------------------------------

    @classmethod
    def _gap_score(
        cls,
        indicator: IndicatorData,
    ) -> tuple[str, float]:

        direction = indicator.gap_direction
        strength = indicator.gap_strength
        score = indicator.gap_strength_score

        if (
            direction is None
            or direction == "NO_GAP"
            or strength is None
        ):
            return "NEUTRAL", 0.0

        score = min(
            cls.MAX_GAP_SCORE,
            max(0.0, float(score)),
        )

        if direction == "GAP_UP":
            return "BUY", score

        if direction == "GAP_DOWN":
            return "SELL", score

        return "NEUTRAL", 0.0

    # ------------------------------------------------------------------
    # ATR Quality
    # ------------------------------------------------------------------

    @classmethod
    def _atr_score(
            cls,
            indicator: IndicatorData,
    ) -> float:

        atr = indicator.atr14
        ltp = indicator.ltp

        if atr is None or ltp is None:
            return 0.0

        atr_value = float(atr)
        ltp_value = float(ltp)

        if atr_value <= 0 or ltp_value <= 0:
            return 0.0

        #
        # ATR as percentage of current price.
        #
        atr_percent = (
                              atr_value / ltp_value
                      ) * 100

        #
        # Extremely low volatility.
        #
        if atr_percent < 0.20:
            return 1.0

        #
        # Healthy intraday volatility.
        #
        if atr_percent < 3.0:
            return 5.0

        #
        # High volatility.
        #
        if atr_percent < 5.0:
            return 3.0

        #
        # Extremely volatile.
        #
        return 1.0

    # ------------------------------------------------------------------
    # Confidence
    # ------------------------------------------------------------------

    @classmethod
    def _confidence_level(
        cls,
        score: float,
    ) -> str:

        if score >= 85:
            return "VERY_HIGH"

        if score >= 70:
            return "HIGH"

        if score >= 50:
            return "MODERATE"

        return "LOW"