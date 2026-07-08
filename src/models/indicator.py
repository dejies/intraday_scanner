from dataclasses import dataclass


@dataclass(slots=True)
class IndicatorData:
    """
    Calculated technical indicators for one symbol.
    """

    ltp: float

    ema20: float | None = None

    ema50: float | None = None

    rsi14: float | None = None

    vwap: float | None = None

    atr14: float | None = None

    average_volume20: float | None = None

    relative_volume: float | None = None