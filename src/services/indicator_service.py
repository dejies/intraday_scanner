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
from src.engines.ema_engine import EMAEngine
from src.engines.macd_engine import MACDEngine
from src.engines.rsi_engine import RSIEngine
from src.engines.vwap_engine import VWAPEngine

from src.models.candle import Candle
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
    ) -> IndicatorData | None:

        if not candles:
            return None

        latest = candles[-1]

        ema9 = EMAEngine.ema9(candles)
        ema20 = EMAEngine.ema20(candles)
        ema50 = EMAEngine.ema50(candles)
        ema200 = EMAEngine.ema200(candles)

        rsi14 = RSIEngine.rsi14(candles)

        macd, signal, histogram = (
            MACDEngine.calculate(candles)
        )

        adx14 = ADXEngine.calculate(candles)

        vwap = VWAPEngine.calculate(candles)

        return IndicatorData(
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
            atr14=None,

            # Volume
            average_volume20=None,
            relative_volume=None,

            updated_at=datetime.utcnow(),
        )