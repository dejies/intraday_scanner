"""
Signal Formatter.

Formats a Signal for dashboard display.
"""

from __future__ import annotations

from src.models.signal import Signal


class SignalFormatter:

    @staticmethod
    def format(
        signal: Signal,
    ) -> list[str]:

        score = signal.score_percentage
        confidence = SignalFormatter._confidence_label(score)

        lines = [

            "SIGNAL ANALYSIS",
            "================",
            "",

            f"Score : {score:.1f}%",
            f"Confidence : {confidence}",

            "",

            "Facts",
            "-----",

        ]

        for fact in signal.analysis_facts:

            lines.append(
                f"• {fact.description}"
            )

        lines.append("")
        lines.append("Breakdown")
        lines.append("---------")

        for name, value in sorted(
            signal.score_breakdown.items()
        ):

            pretty_name = SignalFormatter._pretty_name(
                name
            )

            lines.append(
                f"{pretty_name:<30} +{value}"
            )

        return lines

    @staticmethod
    def format_text(
        signal: Signal,
    ) -> str:

        return "\n".join(
            SignalFormatter.format(signal)
        )

    @staticmethod
    def _confidence_label(
        score: float,
    ) -> str:

        if score >= 80:
            return "Very High"

        elif score >= 65:
            return "High"

        elif score >= 50:
            return "Medium"

        return "Low"

    @staticmethod
    def _pretty_name(
        name: str,
    ) -> str:

        return (
            name.replace("_", " ")
                .title()
        )