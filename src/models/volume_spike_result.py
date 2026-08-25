from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class VolumeSpikeResult:
    """
    Result of Volume Spike analysis.
    """

    #
    # Input
    #
    relative_volume: float

    #
    # Output
    #
    is_spike: bool

    level: str

    #
    # Optional score contribution
    # Used later by Technical Confidence Engine.
    #
    score: int = 0