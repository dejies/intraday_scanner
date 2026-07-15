"""
Signal analysis result.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class AnalysisResult:
    """
    Composite analysis of a stock.

    All scores are normalized to 0-100.
    """

    trend_score: float = 0.0

    momentum_score: float = 0.0

    volume_score: float = 0.0

    price_score: float = 0.0

    session_score: float = 0.0

    pattern_score: float = 0.0

    overall_score: float = 0.0

    reasons: list[str] = field(default_factory=list)

    def calculate(self) -> float:

        self.overall_score = round(
            (
                self.trend_score
                + self.momentum_score
                + self.volume_score
                + self.price_score
                + self.session_score
                + self.pattern_score
            ),
            2,
        )

        return self.overall_score