"""
Alert Formatter.
"""

from __future__ import annotations

from src.alerts import Alert


class AlertFormatter:

    @staticmethod
    def format(
        alert: Alert,
    ) -> str:

        lines = [

            "=" * 60,
            f"{alert.alert_type.value} SIGNAL",
            "=" * 60,
            "",
            f"Symbol      : {alert.symbol}",
            f"Score       : {alert.score:.1f}%",
            f"Confidence  : {alert.level.value.replace('_', ' ').title()}",
            f"Time        : {alert.timestamp:%H:%M:%S}",
            "",
            alert.message,
            "",
            "=" * 60,
        ]

        return "\n".join(lines)