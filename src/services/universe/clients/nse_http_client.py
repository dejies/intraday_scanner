from __future__ import annotations

import time

import requests

from src.services.universe.config import NSEIndexConfig


class NSEHttpClient:
    """
    Thin HTTP client for NSE.

    Responsibilities
    ----------------
    - Download raw content from NSE
    - Retry transient failures
    - Raise only after retries are exhausted
    """

    BASE_URL = "https://www.nseindia.com"

    MAX_RETRIES = 3

    RETRY_DELAY = 1.0

    def __init__(self):

        self._session = requests.Session()

        self._headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "(X11; Linux x86_64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/137.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,"
                      "application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": self.BASE_URL,
        }

        # self.initialize()

    # ---------------------------------------------------------

    def initialize(self) -> None:
        """
        Warm up the NSE session and obtain cookies.
        """

        response = self._session.get(
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

        delay = self.RETRY_DELAY

        last_exception = None

        for attempt in range(1, self.MAX_RETRIES + 1):

            try:

                response = self._session.get(
                    url,
                    headers=self._headers,
                    timeout=30,
                    allow_redirects=True,
                )

                response.raise_for_status()

                return response.text

            except requests.RequestException as ex:

                last_exception = ex

                if attempt == self.MAX_RETRIES:
                    raise

                print(
                    f"NSE request failed "
                    f"(attempt {attempt}/{self.MAX_RETRIES}) "
                    f"for {url}"
                )

                time.sleep(delay)

                delay *= 2

                #
                # Refresh cookies before retry
                #
                time.sleep(delay)
                delay *= 2

        raise last_exception

    # ---------------------------------------------------------

    def download_csv(
        self,
        config: NSEIndexConfig,
    ) -> str:

        return self.get(config.page_url)