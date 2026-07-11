from dataclasses import dataclass

from .candle import Candle


@dataclass(slots=True)
class CandleBuilderState:
    candle: Candle
    last_traded_volume: int