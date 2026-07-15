"""
Scoring Engine.

Converts analysis facts into a confidence score.
"""

from __future__ import annotations

from src.analysis.analysis_fact import (
    AnalysisFact,
    AnalysisFactType,
)

from src.analysis.score_result import (
    ScoreResult,
)

class ScoringEngine:

    WEIGHTS = {

        #
        # Trend
        #
        AnalysisFactType.EMA_BULLISH_ALIGNMENT: 20,

        AnalysisFactType.EMA_BEARISH_ALIGNMENT: 20,

        AnalysisFactType.ADX_STRONG: 10,

        #
        # Momentum
        #
        AnalysisFactType.RSI_BULLISH: 10,
        AnalysisFactType.RSI_BEARISH: 10,

        AnalysisFactType.MACD_BULLISH: 15,
        AnalysisFactType.MACD_BEARISH: 15,

        #
        # Volume
        #
        AnalysisFactType.ABOVE_VWAP: 5,
        AnalysisFactType.BELOW_VWAP: 5,

        AnalysisFactType.RVOL_HIGH: 10,

        #
        # Price
        #
        AnalysisFactType.PRICE_NEAR_EMA20: 10,
        AnalysisFactType.PRICE_NEAR_EMA50: 5,

        #
        # Session
        #
        AnalysisFactType.ORB_BREAKOUT: 5,
        AnalysisFactType.GAP_UP: 5,
        AnalysisFactType.GAP_DOWN: 5,

        #
        # Pattern
        #
        AnalysisFactType.PULLBACK: 10,
    }

    MAX_SCORE = 100

    def score(
            self,
            facts: list[AnalysisFact],
    ) -> ScoreResult:

        result = ScoreResult()

        seen: set[AnalysisFactType] = set()

        for fact in facts:

            if fact.type in seen:
                continue

            seen.add(fact.type)

            weight = self.WEIGHTS.get(
                fact.type,
                0,
            )

            #
            # Keep every fact.
            #
            result.facts.append(fact)

            #
            # Only scored facts contribute.
            #
            if weight > 0:
                result.raw_score += weight

                result.breakdown[
                    fact.type.name
                ] = weight

        result.max_score = self.MAX_SCORE

        result.finalize()

        return result

