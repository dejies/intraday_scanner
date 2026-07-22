from __future__ import annotations

import threading
import time
from src.services.historical_data import HistoricalDataService

class WatchlistMonitor(threading.Thread):

    def __init__(
        self,
        watchlist_service,
        websocket_client,
        instrument_master_service,
        market_data_store,
        candle_builder,
        historical_data_service: HistoricalDataService,
        indicator_service=None,
        scanner=None,
        interval: int = 2,
    ):
        super().__init__(daemon=True)

        self.watchlist_service = watchlist_service
        self.websocket_client = websocket_client
        self.instrument_master_service = instrument_master_service
        self.market_data_store = market_data_store
        self.candle_builder = candle_builder
        self._historical_data_service = historical_data_service
        self.indicator_service = indicator_service
        self.scanner = scanner

        self.interval = interval
        self._running = True

    # ----------------------------------------------------------

    def stop(self) -> None:
        self._running = False

    # ----------------------------------------------------------

    def run(self) -> None:

        while self._running:

            try:

                snapshot = self.watchlist_service.refresh()

                if snapshot is None:
                    time.sleep(self.interval)
                    continue

                # --------------------------------------------------
                # Register newly added instruments
                # --------------------------------------------------

                if snapshot.added:

                    for symbol in snapshot.added:

                        instrument = (
                            self.instrument_master_service.get_by_symbol(
                                symbol
                            )
                        )

                        if instrument is None:
                            continue

                        #
                        # Register runtime state before subscribing.
                        #
                        self.market_data_store.register_instrument(
                            instrument
                        )

                        print(
                            f"Registered: {instrument.symbol} ({instrument.security_id})"
                        )

                        #
                        # Load historical candles and indicators.
                        #
                        self._historical_data_service.load_symbol(
                            instrument
                        )

                        print(
                            f"Historical data loaded: {instrument.symbol}"
                        )

                    added = (
                        self.watchlist_service.get_subscription_tuples(
                            snapshot.added
                        )
                    )

                    self.websocket_client.update_watchlist(
                        added=added,
                        removed=[],
                    )

                # --------------------------------------------------
                # Unsubscribe removed instruments
                # --------------------------------------------------

                if snapshot.removed:

                    removed = (
                        self.watchlist_service.get_subscription_tuples(
                            snapshot.removed
                        )
                    )

                    self.websocket_client.update_watchlist(
                        added=[],
                        removed=removed,
                    )

                    #
                    # Runtime cleanup
                    #
                    for symbol in snapshot.removed:

                        instrument = (
                            self.instrument_master_service.get_by_symbol(
                                symbol
                            )
                        )

                        if instrument is None:
                            continue

                        #
                        # Remove runtime state
                        #
                        self.market_data_store.remove_security(
                            instrument.security_id
                        )

                        #
                        # Remove candle builder state
                        #
                        self.candle_builder.remove_security(
                            instrument.security_id
                        )

                        #
                        # Optional cleanup
                        #
                        if (
                                self.indicator_service is not None
                                and hasattr(
                            self.indicator_service,
                            "remove_symbol",
                        )
                        ):
                            self.indicator_service.remove_symbol(
                                symbol
                            )

                        if (
                                self.scanner is not None
                                and hasattr(
                            self.scanner,
                            "remove_symbol",
                        )
                        ):
                            self.scanner.remove_symbol(
                                symbol
                            )

            except Exception as ex:

                print(
                    f"WatchlistMonitor Error: {ex}"
                )

            time.sleep(self.interval)