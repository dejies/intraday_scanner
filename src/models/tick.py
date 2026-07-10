from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal

@dataclass(slots=True)
class Tick:

    security_id: int

    timestamp: datetime

    ltp: Decimal

    volume: int

    received_at: datetime = field(default_factory=datetime.now)