from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class TechnicalConfidenceResult:
    """
    Result of technical confidence analysis.

    The score represents the strength of the technical
    setup independent of news sentiment.
    """

    score: float

    signal: str

    confidence: str

    trend_score: float = 0.0

    momentum_score: float = 0.0

    macd_score: float = 0.0

    adx_score: float = 0.0

    vwap_score: float = 0.0

    rvol_score: float = 0.0

    volume_spike_score: float = 0.0

    gap_score: float = 0.0

    atr_score: float = 0.0