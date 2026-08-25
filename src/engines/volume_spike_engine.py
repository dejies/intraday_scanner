from __future__ import annotations

from src.models.volume_spike_result import (
    VolumeSpikeResult,
)


class VolumeSpikeEngine:
    """
    Detects abnormal trading volume using Relative Volume (RVOL).
    """

    NORMAL = "NORMAL"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    EXTREME = "EXTREME"

    @classmethod
    def calculate(
            cls,
            relative_volume: float | None,
    ) -> VolumeSpikeResult | None:

        if relative_volume is None:
            return None

        if relative_volume >= 3.0:
            return VolumeSpikeResult(
                relative_volume=relative_volume,
                is_spike=True,
                level=cls.EXTREME,
                score=15,
            )

        if relative_volume >= 2.0:
            return VolumeSpikeResult(
                relative_volume=relative_volume,
                is_spike=True,
                level=cls.HIGH,
                score=10,
            )

        if relative_volume >= 1.2:
            return VolumeSpikeResult(
                relative_volume=relative_volume,
                is_spike=True,
                level=cls.MODERATE,
                score=5,
            )

        return VolumeSpikeResult(
            relative_volume=relative_volume,
            is_spike=False,
            level=cls.NORMAL,
            score=0,
        )