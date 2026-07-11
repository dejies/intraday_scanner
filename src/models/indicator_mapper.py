"""
Maps IndicatorData to IndicatorRecord objects.
"""

from __future__ import annotations

from datetime import datetime

from src.models.indicator import IndicatorData
from src.models.indicator_record import (
    IndicatorRecord,
    IndicatorType,
)


class IndicatorMapper:

    @staticmethod
    def to_records(
        security_id: str,
        timeframe: str,
        candle_time: datetime,
        data: IndicatorData,
    ) -> list[IndicatorRecord]:

        records: list[IndicatorRecord] = []

        def add(indicator: IndicatorType, value: float | None):

            if value is None:
                return

            records.append(
                IndicatorRecord(
                    security_id=security_id,
                    timeframe=timeframe,
                    indicator=indicator,
                    candle_time=candle_time,
                    value=value,
                )
            )

        add(IndicatorType.EMA_9, data.ema9)
        add(IndicatorType.EMA_20, data.ema20)
        add(IndicatorType.EMA_50, data.ema50)
        add(IndicatorType.EMA_200, data.ema200)

        add(IndicatorType.RSI_14, data.rsi14)

        add(IndicatorType.MACD, data.macd)
        add(IndicatorType.MACD_SIGNAL, data.macd_signal)
        add(IndicatorType.MACD_HISTOGRAM, data.macd_histogram)

        add(IndicatorType.ADX_14, data.adx14)

        add(IndicatorType.VWAP, data.vwap)

        return records