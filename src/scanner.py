"""
Scanner Engine

Runs all enabled scanners and collects trading signals.
"""

from __future__ import annotations


from src.services.market_data import MarketData
from src.core.market_data_store import MarketDataStore
from src.services.watchlist import WatchlistService
from src.models.signal import Signal
from src.models.enums import SignalType
from src.services.opening_range_service import OpeningRangeService
from src.services.gap_service import GapService
from src.analysis.scoring_engine import ScoringEngine
from src.ranking.ranking_engine import RankingEngine
from src.alerts.alert_engine import AlertEngine
from src.alerts.alert_formatter import AlertFormatter
from src.alerts.alert_repository import AlertRepository
from src.analysis.signal_analysis_engine import (
    SignalAnalysisEngine,
)
from src.strategies import (
    StrategyManager,
    EMAAlignmentStrategy,
    RSIStrategy,
    MACDStrategy,
    ORBStrategy,
    GapStrategy,
    PullbackStrategy
)
class Scanner:
    """
    Executes all enabled scanners.
    """

    def __init__(
        self,
        market_data: MarketData,
        market_store: MarketDataStore,
        watchlist: WatchlistService,
        opening_range_service: OpeningRangeService,
        gap_service: GapService,
    ) -> None:

        self.market_data = market_data
        self.market_store = market_store
        self.watchlist = watchlist
        self._gap_service = gap_service

        self._alert_repository = AlertRepository()

        self._alert_engine = AlertEngine(
            self._alert_repository
        )

        self._opening_range_service = opening_range_service
        self._strategy_manager = StrategyManager()
        self._ranking_engine = RankingEngine()
        self._strategy_manager.register(
            EMAAlignmentStrategy()
        )
        self._strategy_manager.register(
            RSIStrategy()
        )
        self._strategy_manager.register(
            MACDStrategy()
        )
        self._strategy_manager.register(
            ORBStrategy(
                opening_range_service=self._opening_range_service,
            )
        )

        self._strategy_manager.register(
            GapStrategy(
                gap_service=self._gap_service,
            )
        )

        self._strategy_manager.register(
            PullbackStrategy()
        )

        self._analysis_engine = SignalAnalysisEngine()
        self._scoring_engine = ScoringEngine()

    # ------------------------------------------------------------------

    def scan(self):
        """
        Run all scanners and return trading signals.
        """

        signals: dict[int, Signal] = {}

        for stock in self.market_store.get_all_stocks():

            analysis_facts = self._analysis_engine.analyze(
                stock
            )

            score_result = self._scoring_engine.score(
                analysis_facts
            )

            strategy_results = self._strategy_manager.evaluate(
                stock
            )

            evidence = []

            for result in strategy_results:

                signal = Signal(
                    security_id=stock.instrument.security_id,
                    strategy=result.strategy,
                    signal_type=(
                        SignalType.BUY
                        if result.signal == "BUY"
                        else SignalType.SELL
                    ),
                    signal_price=float(stock.tick.ltp),
                    current_ltp=float(stock.tick.ltp),

                    confidence=score_result.score,

                    raw_score=score_result.raw_score,

                    score_percentage=score_result.percentage,

                    analysis_facts=score_result.facts,

                    score_breakdown=score_result.breakdown,

                    message=result.reason,

                    timestamp=stock.tick.timestamp,
                )

                existing = signals.get(
                    stock.instrument.security_id
                )

                if (
                        existing is None
                        or signal.confidence > existing.confidence
                ):
                    signals[
                        stock.instrument.security_id
                    ] = signal

        all_signals = list(
            signals.values()
        )

        buy_ranked = self._ranking_engine.rank_buy(
            all_signals
        )

        sell_ranked = self._ranking_engine.rank_sell(
            all_signals
        )

        # for ranked_signal in buy_ranked + sell_ranked:
        #
        #     alert = self._alert_engine.process(
        #         ranked_signal.signal
        #     )
        #
        #     if alert is not None:
        #         print(
        #             AlertFormatter.format(alert)
        #         )

        for ranked in buy_ranked:
            self.market_store.update_signal(
                ranked.signal
            )

        for ranked in sell_ranked:
            self.market_store.update_signal(
                ranked.signal
            )

        return all_signals

    @property
    def strategy_manager(self) -> StrategyManager:
        return self._strategy_manager