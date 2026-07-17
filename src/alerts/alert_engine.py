"""
Alert Engine.
"""

from __future__ import annotations

from datetime import datetime

from src.alerts.alert import Alert
from src.alerts.alert_level import AlertLevel
from src.alerts.alert_level import AlertLevel
from src.alerts.alert_repository import AlertRepository
from src.alerts.alert_type import AlertType
from src.models.enums import SignalType
from src.models.signal import Signal


class AlertEngine:

    def __init__(
        self,
        repository: AlertRepository,
    ) -> None:

        self._repository = repository

    # ---------------------------------------------------------

    def process(
        self,
        signal: Signal,
    ) -> Alert | None:

        previous = self._repository.get(
            str(signal.security_id)
        )

        #
        # Ignore duplicate or weaker alerts.
        #
        if previous is not None:

            if signal.score_percentage <= previous.score:
                return None

        level = self._alert_level(
            signal.score_percentage
        )

        alert_type = (
            AlertType.BUY
            if signal.signal_type == SignalType.BUY
            else AlertType.SELL
        )

        alert = Alert(
            symbol=str(signal.security_id),
            alert_type=alert_type,
            level=level,
            score=signal.score_percentage,
            message=f"{alert_type.value} Signal",
            timestamp=datetime.now(),
        )

        self._repository.save(alert)

        return alert

    # ---------------------------------------------------------

    @staticmethod
    def _alert_level(
        score: float,
    ) -> AlertLevel:

        if score >= 80:
            return AlertLevel.VERY_HIGH

        if score >= 65:
            return AlertLevel.HIGH

        if score >= 50:
            return AlertLevel.MEDIUM

        return AlertLevel.LOW