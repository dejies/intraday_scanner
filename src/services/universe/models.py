from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class UniverseStock:

    symbol: str

    company_name: str

    security_id: str | None = None

    exchange_segment: str | None = None

    index_name: str = ""