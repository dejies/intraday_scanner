"""
Result returned by the scoring engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from src.analysis.analysis_fact import AnalysisFact


@dataclass(slots=True)
class ScoreResult:

    #
    # Maximum possible score
    #
    max_score: float = 100.0

    #
    # Sum of all scoring rules
    #
    raw_score: float = 0.0

    #
    # Final score after normalization/capping
    #
    score: float = 0.0

    #
    # Final percentage
    #
    percentage: float = 0.0

    #
    # Facts contributing
    #
    facts: list[AnalysisFact] = field(
        default_factory=list
    )

    #
    # Score contribution
    #
    breakdown: dict[str, float] = field(
        default_factory=dict
    )

    def finalize(self) -> None:

        #
        # Final score
        #
        self.score = min(
            self.raw_score,
            self.max_score,
        )

        #
        # Percentage
        #
        if self.max_score > 0:

            self.percentage = round(
                (self.score / self.max_score) * 100,
                2,
            )