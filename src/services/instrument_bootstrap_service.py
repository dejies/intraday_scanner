from __future__ import annotations

from src.services.historical_data import HistoricalDataService
from src.services.instrument_state_service import (
    InstrumentStateService,
)

class InstrumentBootstrapService:
    """
    Handles the complete runtime lifecycle of an instrument.

    Responsibilities
    ----------------
    - Register runtime state
    - Load historical candles
    - Initialize indicators

    Cleanup
    -------
    - Remove runtime state
    - Remove candle builder state
    - Remove indicator state
    - Remove scanner state
    """

    def __init__(
            self,
            market_data_store,
            candle_builder,
            historical_data_service,
            state_service: InstrumentStateService,
            indicator_service=None,
            scanner=None,
    ):
        self._state_service = state_service
        self._market_data_store = market_data_store
        self._candle_builder = candle_builder
        self._historical_data_service = historical_data_service
        self._indicator_service = indicator_service
        self._scanner = scanner

    # ---------------------------------------------------------

    def initialize(
            self,
            instrument,
    ) -> bool:
        """
        Initialize runtime state.

        Returns
        -------
        True
            Instrument was initialized.

        False
            Instrument was already initialized.
        """

        if self._state_service.is_ready(
                instrument.security_id,
        ):
            return False

        #
        # Register runtime state.
        #
        self._market_data_store.register_instrument(
            instrument
        )

        #
        # Load historical candles + indicators.
        #
        self._historical_data_service.load_symbol(
            instrument
        )

        #
        # Mark ready.
        #
        self._state_service.mark_ready(
            instrument.security_id,
        )

        return True

    # ---------------------------------------------------------

    def cleanup(
        self,
        instrument,
    ) -> None:
        """
        Remove all runtime state for an instrument.
        """

        #
        # Remove runtime state.
        #
        self._market_data_store.remove_security(
            instrument.security_id
        )

        #
        # Remove candle builder state.
        #
        self._candle_builder.remove_security(
            instrument.security_id
        )

        #
        # Optional indicator cleanup.
        #
        if (
            self._indicator_service is not None
            and hasattr(
                self._indicator_service,
                "remove_symbol",
            )
        ):
            self._indicator_service.remove_symbol(
                instrument.symbol
            )

        #
        # Optional scanner cleanup.
        #
        if (
            self._scanner is not None
            and hasattr(
                self._scanner,
                "remove_symbol",
            )
        ):
            self._scanner.remove_symbol(
                instrument.symbol
            )

        self._state_service.remove(
            instrument.security_id,
        )