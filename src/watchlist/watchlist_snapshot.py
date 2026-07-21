from dataclasses import dataclass


@dataclass(slots=True)
class WatchlistSnapshot:
    symbols: set[str]
    added: set[str]
    removed: set[str]