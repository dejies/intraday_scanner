"""
Alert Repository.

Maintains alert state to avoid duplicate alerts.
"""

from __future__ import annotations

from src.alerts.alert import Alert


class AlertRepository:

    def __init__(self) -> None:

        self._alerts: dict[str, Alert] = {}

    # -------------------------------------------------------------

    def exists(
        self,
        symbol: str,
    ) -> bool:

        return symbol in self._alerts

    # -------------------------------------------------------------

    def get(
        self,
        symbol: str,
    ) -> Alert | None:

        return self._alerts.get(symbol)

    # -------------------------------------------------------------

    def save(
        self,
        alert: Alert,
    ) -> None:

        self._alerts[alert.symbol] = alert

    # -------------------------------------------------------------

    def remove(
        self,
        symbol: str,
    ) -> None:

        self._alerts.pop(symbol, None)

    # -------------------------------------------------------------

    def clear(self) -> None:

        self._alerts.clear()

    # -------------------------------------------------------------

    def count(self) -> int:

        return len(self._alerts)

    # -------------------------------------------------------------

    def all(self) -> list[Alert]:

        return list(self._alerts.values())