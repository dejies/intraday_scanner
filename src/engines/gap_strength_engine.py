from __future__ import annotations

from src.models import GapDirection
from src.models import Gap
from src.models.gap_strength_result import GapStrengthResult


class GapStrengthEngine:
    """
    Calculates gap strength relative to ATR.

    The engine does not detect gaps.
    It receives an existing Gap object and ATR14
    and determines the relative strength of the gap.
    """

    NO_GAP = "NO_GAP"

    GAP_UP = "GAP_UP"
    GAP_DOWN = "GAP_DOWN"

    WEAK = "WEAK"
    MODERATE = "MODERATE"
    STRONG = "STRONG"
    VERY_STRONG = "VERY_STRONG"

    WEAK_THRESHOLD = 0.25
    MODERATE_THRESHOLD = 0.50
    STRONG_THRESHOLD = 1.00

    WEAK_SCORE = 2
    MODERATE_SCORE = 5
    STRONG_SCORE = 8
    VERY_STRONG_SCORE = 12

    @classmethod
    def calculate(
        cls,
        gap: Gap | None,
        atr14: float | None,
    ) -> GapStrengthResult | None:
        """
        Calculate gap strength relative to ATR.

        Parameters
        ----------
        gap:
            Existing gap information produced by GapService.

        atr14:
            ATR14 value.

        Returns
        -------
        GapStrengthResult | None
        """

        if gap is None or atr14 is None:
            return None

        if atr14 <= 0:
            return None

        #
        # Calculate actual price gap.
        #
        gap_amount = (
            gap.today_open - gap.previous_close
        )

        #
        # Use the gap already calculated by GapService.
        #
        gap_percent = gap.gap_percent

        #
        # No meaningful gap.
        #
        if gap.direction == GapDirection.NONE:
            return GapStrengthResult(
                gap_percent=round(gap_percent, 2),
                atr14=round(atr14, 2),
                gap_atr_ratio=0.0,
                direction=cls.NO_GAP,
                strength=cls.NO_GAP,
                score=0,
            )

        #
        # Determine direction.
        #
        direction = (
            cls.GAP_UP
            if gap_amount > 0
            else cls.GAP_DOWN
        )

        #
        # Compare the actual price gap with ATR.
        #
        gap_atr_ratio = (
            abs(gap_amount) / atr14
        )

        #
        # Classify strength.
        #
        if gap_atr_ratio >= cls.STRONG_THRESHOLD:

            strength = cls.VERY_STRONG
            score = cls.VERY_STRONG_SCORE

        elif gap_atr_ratio >= cls.MODERATE_THRESHOLD:

            strength = cls.STRONG
            score = cls.STRONG_SCORE

        elif gap_atr_ratio >= cls.WEAK_THRESHOLD:

            strength = cls.MODERATE
            score = cls.MODERATE_SCORE

        else:

            strength = cls.WEAK
            score = cls.WEAK_SCORE

        return GapStrengthResult(
            gap_percent=round(gap_percent, 2),
            atr14=round(atr14, 2),
            gap_atr_ratio=round(gap_atr_ratio, 2),
            direction=direction,
            strength=strength,
            score=score,
        )