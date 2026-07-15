"""
Coordinates candle building and persistence.
"""

from __future__ import annotations

from src.services.indicator_service import IndicatorService
from src.models import CandleBuilderResult
from src.models import Candle
from src.builders import CandleBuilder
from src.repositories import CandleRepository
from src.models.tick import Tick
from src.models.indicator_mapper import IndicatorMapper
from src.repositories import IndicatorRepository
from src.core.market_data_store import MarketDataStore
from src.services.opening_range_service import OpeningRangeService


class CandleService:

    def __init__(
            self,
            builder: CandleBuilder,
            repository: CandleRepository,
            indicator_repository: IndicatorRepository,
            indicator_service: IndicatorService,
            market_data_store: MarketDataStore,
            opening_range_service: OpeningRangeService,
    ):
        self._builder = builder
        self._repository = repository
        self._indicator_repository = indicator_repository
        self._indicator_service = indicator_service
        self._market_data_store = market_data_store
        self._opening_range_service = opening_range_service

    # ---------------------------------------------------------

    def process_tick(
        self,
        tick: Tick,
    ) -> CandleBuilderResult:

        result = self._builder.process_tick(tick)

        #
        # Persist current (forming) candle.
        #
        self._repository.upsert(
            result.current_candle
        )

        #
        # Persist completed candles and calculate indicators.
        #
        for candle in result.completed_candles:

            self._repository.upsert(candle)

            history = self._repository.history(
                candle.security_id,
                candle.interval,
                limit=250,
            )

            indicator_data = self._indicator_service.calculate(
                history,
            )

            if indicator_data is not None:
                records = IndicatorMapper.to_records(
                    security_id=candle.security_id,
                    timeframe=candle.interval.value,
                    candle_time=candle.candle_time,
                    data=indicator_data,
                )

                self._indicator_repository.insert_many(records)
                self._market_data_store.set_indicator_data(
                    candle.security_id,
                    indicator_data,
                )
            self._opening_range_service.process_candle(
                candle
            )

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