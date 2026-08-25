from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class GapStrengthResult:
    """
    Result of gap strength analysis.
    """

    gap_percent: float

    atr14: float

    gap_atr_ratio: float

    direction: str

    strength: str

    score: int = 0