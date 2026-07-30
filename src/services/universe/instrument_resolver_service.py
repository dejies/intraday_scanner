from __future__ import annotations

from src.services.universe.models import (
    MarketUniverse,
    UniverseMembership,
    UniverseStock,
)


class InstrumentResolverService:
    """
    Resolves instrument metadata using InstrumentMasterService.

    Responsibilities
    ----------------
    - Resolve security_id
    - Resolve exchange_segment

    Knows NOTHING about

    - SQLite
    - NSE
    - Scanner
    """

    def __init__(
        self,
        instrument_master_service,
    ):
        self._instrument_master = instrument_master_service

    # ---------------------------------------------------------

    def resolve(
        self,
        universe: MarketUniverse,
    ) -> MarketUniverse:

        resolved = MarketUniverse()

        #
        # Resolve stocks
        #
        for stock in universe.stocks.values():

            instrument = self._instrument_master.get_by_symbol(
                stock.symbol
            )

            if instrument is None:
                #
                # Ignore symbols that are not
                # available in Instrument Master.
                #
                continue

            resolved.add_stock(

                UniverseStock(

                    symbol=stock.symbol,

                    company_name=stock.company_name,

                    security_id=str(
                        instrument.security_id
                    ),

                    exchange_segment=instrument.exchange_segment,
                )
            )

        #
        # Copy memberships only for resolved symbols
        #
        valid_symbols = resolved.symbols()

        for membership in universe.memberships:

            if membership.symbol in valid_symbols:

                resolved.add_membership(
                    membership
                )

        return resolved