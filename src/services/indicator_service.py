"""
Indicator Service.

Responsibilities
----------------
- Orchestrate indicator calculation
- Return latest IndicatorData
- No database persistence
"""

from __future__ import annotations

from datetime import datetime

from src.engines.adx_engine import ADXEngine
from src.engines.atr_engine import ATREngine
from src.engines.ema_engine import EMAEngine
from src.engines.gap_strength_engine import GapStrengthEngine
from src.engines.macd_engine import MACDEngine
from src.engines.rsi_engine import RSIEngine
from src.engines.rvol_engine import RVOLEngine
from src.engines.technical_confidence_engine import (
    TechnicalConfidenceEngine,
)
from src.engines.volume_spike_engine import VolumeSpikeEngine
from src.engines.vwap_engine import VWAPEngine

from src.models.candle import Candle
from src.models.gap import Gap
from src.models.indicator import IndicatorData


class IndicatorService:
    """
    Calculates technical indicators from candle history.

    This service performs calculations only.
    Persistence is handled by IndicatorRepository.
    """

    # ------------------------------------------------------------------

    def calculate(
        self,
        candles: list[Candle],
        gap: Gap | None = None,
    ) -> IndicatorData | None:

        if not candles:
            return None

        latest = candles[-1]

        # ------------------------------------------------------------------
        # Trend
        # ------------------------------------------------------------------

        ema9 = EMAEngine.ema9(candles)
        ema20 = EMAEngine.ema20(candles)
        ema50 = EMAEngine.ema50(candles)
        ema200 = EMAEngine.ema200(candles)

        # ------------------------------------------------------------------
        # Momentum
        # ------------------------------------------------------------------

        rsi14 = RSIEngine.rsi14(candles)

        macd, signal, histogram = (
            MACDEngine.calculate(candles)
        )

        # ------------------------------------------------------------------
        # Trend Strength
        # ------------------------------------------------------------------

        adx14 = ADXEngine.calculate(candles)

        # ------------------------------------------------------------------
        # Volatility
        # ------------------------------------------------------------------

        atr14 = ATREngine.calculate(candles)

        # ------------------------------------------------------------------
        # Intraday
        # ------------------------------------------------------------------

        vwap = VWAPEngine.calculate(candles)

        # ------------------------------------------------------------------
        # Volume
        # ------------------------------------------------------------------

        rvol_data = RVOLEngine.calculate(candles)

        # ------------------------------------------------------------------
        # Volume Spike
        # ------------------------------------------------------------------

        volume_spike = None

        if rvol_data is not None:

            volume_spike = VolumeSpikeEngine.calculate(
                rvol_data.rvol
            )

        # ------------------------------------------------------------------
        # Gap Strength
        # ------------------------------------------------------------------

        gap_strength = None

        if gap is not None and atr14 is not None:

            gap_strength = GapStrengthEngine.calculate(
                gap=gap,
                atr14=atr14,
            )

        # ------------------------------------------------------------------
        # Build IndicatorData
        #
        # TechnicalConfidenceEngine consumes IndicatorData, so calculate
        # the base indicator data first and then calculate confidence.
        # ------------------------------------------------------------------

        indicator_data = IndicatorData(
            ltp=float(latest.close),

            # Trend
            ema9=ema9,
            ema20=ema20,
            ema50=ema50,
            ema200=ema200,

            # Momentum
            rsi14=rsi14,

            # MACD
            macd=macd,
            macd_signal=signal,
            macd_histogram=histogram,

            # Trend Strength
            adx14=adx14,

            # Intraday
            vwap=vwap,

            # Volatility
            atr14=atr14,

            # Volume
            average_volume20=(
                rvol_data.average_volume
                if rvol_data
                else None
            ),

            relative_volume=(
                rvol_data.rvol
                if rvol_data
                else None
            ),

            # Volume Spike
            has_volume_spike=(
                volume_spike.is_spike
                if volume_spike
                else None
            ),

            volume_spike_level=(
                volume_spike.level
                if volume_spike
                else None
            ),

            volume_spike_score=(
                volume_spike.score
                if volume_spike
                else 0
            ),

            # Gap Strength
            gap_percent=(
                gap_strength.gap_percent
                if gap_strength
                else None
            ),

            gap_direction=(
                gap_strength.direction
                if gap_strength
                else None
            ),

            gap_strength=(
                gap_strength.strength
                if gap_strength
                else None
            ),

            gap_atr_ratio=(
                gap_strength.gap_atr_ratio
                if gap_strength
                else None
            ),

            gap_strength_score=(
                gap_strength.score
                if gap_strength
                else 0
            ),

            updated_at=datetime.utcnow(),
        )

        # ------------------------------------------------------------------
        # Technical Confidence
        # ------------------------------------------------------------------

        technical_confidence = (
            TechnicalConfidenceEngine.calculate(
                indicator_data
            )
        )

        # ------------------------------------------------------------------
        # Add Technical Confidence to IndicatorData
        # ------------------------------------------------------------------

        if technical_confidence is not None:

            indicator_data.technical_score = (
                technical_confidence.score
            )

            indicator_data.technical_signal = (
                technical_confidence.signal
            )

            indicator_data.technical_confidence = (
                technical_confidence.confidence
            )

        return indicator_data