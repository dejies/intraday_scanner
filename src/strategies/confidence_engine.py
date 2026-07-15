"""
Confidence Engine.

Builds a single confidence score from strategy evidence.
"""

from __future__ import annotations

from src.strategies.evidence import (
    EvidenceType,
    SignalEvidence,
)


class ConfidenceEngine:

    #
    # Evidence weights
    #
    WEIGHTS = {

        EvidenceType.EMA_ALIGNMENT: 20,

        EvidenceType.MACD_BULLISH: 15,
        EvidenceType.MACD_BEARISH: 15,

        EvidenceType.RSI_BULLISH: 10,
        EvidenceType.RSI_BEARISH: 10,

        EvidenceType.ADX_STRONG: 10,

        EvidenceType.ABOVE_VWAP: 5,
        EvidenceType.BELOW_VWAP: 5,

        EvidenceType.ORB_BREAKOUT: 20,

        EvidenceType.GAP_CONTINUATION: 15,

        EvidenceType.PULLBACK: 15,
    }

    MAX_SCORE = 100.0

    # ---------------------------------------------------------

    def calculate(
        self,
        evidence: list[SignalEvidence],
    ) -> float:

        #
        # Prevent duplicate evidence.
        #
        unique = {
            item.evidence: item
            for item in evidence
        }

        score = 0.0

        for item in unique.values():

            score += self.WEIGHTS.get(
                item.evidence,
                0.0,
            )

        return min(
            score,
            self.MAX_SCORE,
        )

    # ---------------------------------------------------------

    def descriptions(
        self,
        evidence: list[SignalEvidence],
    ) -> list[str]:

        seen: set[EvidenceType] = set()

        descriptions: list[str] = []

        for item in evidence:

            if item.evidence in seen:
                continue

            seen.add(item.evidence)

            descriptions.append(
                item.description
            )

        return descriptions