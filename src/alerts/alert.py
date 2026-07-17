from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.alerts.alert_level import AlertLevel
from src.alerts.alert_type import AlertType


@dataclass(slots=True)
class Alert:

    symbol: str

    alert_type: AlertType

    level: AlertLevel

    score: float

    message: str

    timestamp: datetime