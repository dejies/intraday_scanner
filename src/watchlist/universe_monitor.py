from __future__ import annotations

import threading
import time

from src.services.instrument_bootstrap_service import (
    InstrumentBootstrapService,
)

# Move this to config.py later
BOOTSTRAP_BATCH_SIZE = 10


class UniverseMonitor(threading.Thread):

    def __init__(
        self,
        watchlist_service,
        websocket_client,
        instrument_master_service,
        bootstrap_service: InstrumentBootstrapService,
        state_service,
        interval: int = 2,
    ):
        super().__init__(daemon=True)

        self._first_run = True
        self._running = True

        self.watchlist_service = watchlist_service
        self.websocket_client = websocket_client
        self.instrument_master_service = (
            instrument_master_service
        )
        self.bootstrap_service = bootstrap_service
        self.state_service = state_service

        self.interval = interval

    # ---------------------------------------------------------

    def stop(self):

        self._running = False

    # ---------------------------------------------------------

    def run(self):

        while self._running:

            try:

                #
                # Refresh watchlist
                #
                if self._first_run:

                    snapshot = self.watchlist_service.load()
                    self._first_run = False

                else:

                    snapshot = self.watchlist_service.refresh()

                #
                # Bootstrap instruments that are not ready.
                #
                initialized_symbols = []

                initialized = 0

                for instrument in self.watchlist_service.get_all():

                    if initialized >= BOOTSTRAP_BATCH_SIZE:
                        break

                    #
                    # initialize() returns True only when a new
                    # instrument is successfully bootstrapped.
                    #
                    if self.bootstrap_service.initialize(
                        instrument
                    ):
                        initialized_symbols.append(
                            instrument.symbol
                        )
                        initialized += 1

                #
                # Subscribe newly initialized instruments.
                #
                if initialized_symbols:

                    added = (
                        self.watchlist_service.get_subscription_tuples(
                            set(initialized_symbols)
                        )
                    )

                    self.websocket_client.update_watchlist(
                        added=added,
                        removed=[],
                    )

                #
                # Handle removals immediately.
                #
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

                    for symbol in sorted(snapshot.removed):

                        instrument = (
                            self.instrument_master_service.get_by_symbol(
                                symbol
                            )
                        )

                        if instrument is None:
                            continue

                        self.bootstrap_service.cleanup(
                            instrument
                        )

            except Exception as ex:

                print(
                    f"UniverseMonitor Error: {ex}"
                )

            end_time = time.time() + self.interval

            while (
                self._running
                and time.time() < end_time
            ):
                time.sleep(0.1)