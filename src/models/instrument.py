"""
Instrument Model.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Instrument:
    """
    Represents one instrument from the
    Dhan Instrument Master.
    """

    security_id: int

    exchange: str

    segment: str

    instrument_type: str

    symbol: str

    custom_symbol: str

    company_name: str

    lot_size: float

    tick_size: float

    series: str | None = None

    expiry_date: str | None = None

    strike_price: float | None = None

    option_type: str | None = None