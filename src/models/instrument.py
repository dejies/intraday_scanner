"""
Instrument Model.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from datetime import date

@dataclass(frozen=True, slots=True)
class Instrument:
    """
    Represents one instrument from the
    Dhan Instrument Master.

    This is immutable reference data loaded once during
    application startup.
    """

    security_id: int

    exchange: str

    segment: str

    instrument_type: str

    symbol: str

    custom_symbol: str

    company_name: str

    lot_size: int

    tick_size: Decimal

    series: str | None = None

    expiry_date: date | None = None

    strike_price: Decimal | None = None

    option_type: str | None = None