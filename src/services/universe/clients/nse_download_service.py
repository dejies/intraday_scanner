from __future__ import annotations

import re
from urllib.parse import urljoin

from src.services.universe.clients import NSEHttpClient
from src.services.universe.config import NSEIndexConfig


class NSEDownloadService:
    """
    Downloads raw CSV data for NSE indices.

    Responsibilities
    ----------------
    1. Download the index page.
    2. Locate the CSV download link.
    3. Download the CSV.
    4. Return CSV text.

    Knows NOTHING about:
    - Universe models
    - SQLite
    - Scanner
    - Dashboard
    """

    def __init__(
        self,
        client: NSEHttpClient,
    ):
        self._client = client

    # ---------------------------------------------------------

    def download_index(
        self,
        config: NSEIndexConfig,
    ) -> str:

        #
        # Download HTML page
        #
        html = self._client.get(
            config.page_url
        )

        print("PAGE :", config.index_name, config.page_url)
        #
        # Locate CSV link
        #
        csv_url = self._extract_csv_url(
            html,
            config.page_url,
        )

        print("CSV  :", csv_url)
        #
        # Download CSV
        #
        return self._client.get(
            csv_url
        )

    # ---------------------------------------------------------

    def _extract_csv_url(
        self,
        html: str,
        base_url: str,
    ) -> str:

        #
        # Absolute URL
        #
        match = re.search(
            r'https://[^"\']+\.csv',
            html,
            re.IGNORECASE,
        )

        if match:
            return match.group(0)

        #
        # Relative URL
        #
        match = re.search(
            r'href=["\']([^"\']+\.csv)["\']',
            html,
            re.IGNORECASE,
        )

        if match:
            return urljoin(
                base_url,
                match.group(1),
            )

        raise RuntimeError(
            "Unable to locate CSV download link "
            f"for {base_url}"
        )