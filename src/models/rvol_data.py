from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class RVOLData:
    """
    Relative Volume (RVOL) calculated for a completed candle.

    current_volume : Volume of the latest completed candle.

    average_volume : Average volume over the configured lookback period.

    rvol : current_volume / average_volume

    classification :
        LOW
        NORMAL
        HIGH
        VERY_HIGH
    """

    symbol: str
    timestamp: datetime

    current_volume: float
    average_volume: float

    rvol: float
    classification: str