from __future__ import annotations

import threading


class InstrumentStateService:
    """
    Tracks the runtime initialization state of instruments.

    States
    ------
    - READY : Instrument has completed bootstrap.

    This service makes InstrumentBootstrapService idempotent by
    preventing repeated initialization of the same instrument.
    """

    def __init__(self):
        self._ready: set[int] = set()
        self._lock = threading.RLock()

    # ---------------------------------------------------------

    def is_ready(
        self,
        security_id: int,
    ) -> bool:
        """
        Returns True if the instrument has already been initialized.
        """

        with self._lock:
            return security_id in self._ready

    # ---------------------------------------------------------

    def mark_ready(
        self,
        security_id: int,
    ) -> None:
        """
        Marks an instrument as initialized.
        """

        with self._lock:
            self._ready.add(security_id)

    # ---------------------------------------------------------

    def remove(
        self,
        security_id: int,
    ) -> None:
        """
        Removes an instrument from the initialized set.
        """

        with self._lock:
            self._ready.discard(security_id)

    # ---------------------------------------------------------

    def clear(self) -> None:
        """
        Clears all runtime state.
        """

        with self._lock:
            self._ready.clear()

    # ---------------------------------------------------------

    def count(self) -> int:
        """
        Returns the number of initialized instruments.
        """

        with self._lock:
            return len(self._ready)

    # ---------------------------------------------------------

    def ready_security_ids(self) -> set[int]:
        """
        Returns a copy of initialized security IDs.
        """

        with self._lock:
            return set(self._ready)