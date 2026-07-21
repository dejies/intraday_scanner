from __future__ import annotations

from typing import Iterable

from src.models.instrument import Instrument


class InstrumentResolver:
    """
    Resolves stock symbols into Dhan subscription tuples.

    Output format:
        (exchange_segment, security_id, request_code)
    """

    def __init__(self, instrument_service):

        self.instrument_service = instrument_service

    def resolve(self, symbols: Iterable[str]) -> list[tuple]:

        subscriptions: list[tuple] = []

        for symbol in sorted(symbols):

            instrument: Instrument | None = (
                self.instrument_service.get_by_symbol(symbol)
            )

            if instrument is None:
                continue

            subscriptions.append(
                (
                    instrument.exchange_segment,
                    instrument.security_id,
                    15,  # Ticker
                )
            )

        return subscriptions