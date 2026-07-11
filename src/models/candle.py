from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from .candle_interval import CandleInterval

@dataclass(slots=True)
class Candle:
    security_id: str
    interval: CandleInterval

    candle_time: datetime

    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal

    volume: int

    is_closed: bool = False