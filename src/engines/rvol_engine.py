from __future__ import annotations

from statistics import mean

from src.models.candle import Candle
from src.models.rvol_data import RVOLData


class RVOLEngine:
    """
    Calculates Relative Volume (RVOL).

    RVOL = Current Candle Volume / Average Volume (last 20 completed candles)
    """

    LOOKBACK = 20

    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"

    @classmethod
    def calculate(
        cls,
        candles: list[Candle],
    ) -> RVOLData | None:
        """
        Parameters
        ----------
        candles
            Complete candle history including the latest completed candle.

        Returns
        -------
        RVOLData | None
        """

        # Need 20 previous candles + current candle
        if len(candles) < cls.LOOKBACK + 1:
            return None

        latest = candles[-1]
        history = candles[-(cls.LOOKBACK + 1):-1]

        average_volume = mean(c.volume for c in history)

        if average_volume <= 0:
            return None

        rvol = latest.volume / average_volume

        return RVOLData(
            symbol=str(getattr(latest, "symbol", None)),
            timestamp=latest.candle_time,
            current_volume=latest.volume,
            average_volume=average_volume,
            rvol=round(rvol, 2),
            classification=cls.classify(rvol),
        )

    @classmethod
    def classify(cls, rvol: float) -> str:

        if rvol < 0.8:
            return cls.LOW

        if rvol < 1.2:
            return cls.NORMAL

        if rvol < 2.0:
            return cls.HIGH

        return cls.VERY_HIGH