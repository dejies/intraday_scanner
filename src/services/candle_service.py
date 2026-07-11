"""
Coordinates candle building and persistence.
"""

from __future__ import annotations

from src.models import CandleBuilderResult
from src.models import Candle
from src.builders import CandleBuilder
from src.repositories import CandleRepository
from src.models.tick import Tick

class CandleService:

    def __init__(
        self,
        builder: CandleBuilder,
        repository: CandleRepository,
    ):
        self._builder = builder
        self._repository = repository

    # ---------------------------------------------------------

    def process_tick(
            self,
            tick: Tick,
    ) -> CandleBuilderResult:
        result = self._builder.process_tick(tick)

        self._repository.upsert(
            result.current_candle
        )

        for candle in result.completed_candles:
            self._repository.upsert(candle)

        return result

    # ---------------------------------------------------------

    def current_candle(
        self,
        security_id: str,
    ) -> Candle | None:

        return self._builder.current_candle(
            security_id
        )

    # ---------------------------------------------------------

    def reset(self):

        self._builder.reset()

    # ---------------------------------------------------------

    def remove_security(
        self,
        security_id: str,
    ):

        self._builder.remove_security(
            security_id
        )

