from dataclasses import dataclass

from .candle import Candle

@dataclass(slots=True)
class CandleBuilderResult:
    current_candle: Candle
    completed_candles: list[Candle]