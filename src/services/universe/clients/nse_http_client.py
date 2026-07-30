from __future__ import annotations

import requests

from src.services.universe.config import NSEIndexConfig


class NSEHttpClient:
    """
    Thin HTTP client for NSE.

    Responsibilities
    ----------------
    - Download raw content from NSE
    - Raise HTTP errors

    Knows NOTHING about:
    - MarketUniverse
    - Repository
    - Scanner
    """

    BASE_URL = "https://www.nseindia.com"

    def __init__(self):
        self._headers = {
            "User-Agent": "Mozilla/5.0",
        }

    # ---------------------------------------------------------

    def initialize(self):
        """
        Warm up connectivity to NSE.
        """

        response = requests.get(
            self.BASE_URL,
            headers=self._headers,
            timeout=20,
            allow_redirects=True,
        )

        response.raise_for_status()

    # ---------------------------------------------------------

    def get(
        self,
        url: str,
    ) -> str:

        response = requests.get(
            url,
            headers=self._headers,
            timeout=30,
            allow_redirects=True,
        )

        response.raise_for_status()

        return response.text

    # ---------------------------------------------------------

    def download_csv(
        self,
        config: NSEIndexConfig,
    ) -> str:

        return self.get(config.page_url)