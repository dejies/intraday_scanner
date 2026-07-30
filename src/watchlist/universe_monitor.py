from __future__ import annotations

import threading
import time

from src.services.instrument_bootstrap_service import (
    InstrumentBootstrapService,
)


class UniverseMonitor(threading.Thread):

    def __init__(
        self,
        watchlist_service,
        websocket_client,
        instrument_master_service,
        bootstrap_service: InstrumentBootstrapService,
        interval: int = 2,
    ):
        super().__init__(daemon=True)

        self.watchlist_service = watchlist_service
        self.websocket_client = websocket_client
        self.instrument_master_service = (
            instrument_master_service
        )
        self.bootstrap_service = bootstrap_service

        self.interval = interval
        self._running = True

    # ---------------------------------------------------------

    def stop(self):

        self._running = False

    # ---------------------------------------------------------

    def run(self):

        while self._running:

            try:

                snapshot = self.watchlist_service.refresh()

                #
                # No changes.
                #
                if (
                    not snapshot.added
                    and not snapshot.removed
                ):
                    end_time = time.time() + self.interval

                    while self._running and time.time() < end_time:
                        time.sleep(0.1)
                    continue

                #
                # Added
                #
                if snapshot.added:

                    for symbol in sorted(snapshot.added):

                        instrument = (
                            self.instrument_master_service.get_by_symbol(
                                symbol
                            )
                        )

                        if instrument is None:
                            continue

                        self.bootstrap_service.initialize(
                            instrument
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

                #
                # Removed
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

            while self._running and time.time() < end_time:
                time.sleep(0.1)