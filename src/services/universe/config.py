from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NSEIndexConfig:

    index_name: str

    page_url: str


NIFTY500 = NSEIndexConfig(
    index_name="NIFTY500",
    page_url="https://www.nseindia.com/static/products-services/indices-nifty500-index",
)

MIDCAP150 = NSEIndexConfig(
    index_name="MIDCAP150",
    page_url="https://www.nseindia.com/static/products-services/indices-niftymidcap150-index",
)

SMALLCAP250 = NSEIndexConfig(
    index_name="SMALLCAP250",
    page_url="https://www.nseindia.com/static/products-services/indices-niftysmallcap250-index",
)