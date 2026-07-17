"""
Ranked Signal.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.models.signal import Signal


@dataclass(slots=True)
class RankedSignal:

    #
    # Original signal
    #
    signal: Signal

    #
    # Overall rank
    #
    rank: int = 0

    #
    # Score used for ranking
    #
    score: float = 0.0