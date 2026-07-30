from __future__ import annotations

from src.services.universe.clients import NSEHttpClient
from src.services.universe.config import NSEIndexConfig


class NSEDownloadService:
    """
    Responsible for downloading raw CSV files from NSE.

    Knows NOTHING about:
    - Universe models
    - Repository
    - Scanner
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
        """
        Returns raw CSV text for an index.
        """

        #
        # Future enhancement:
        #
        # This method is the ONLY place that should
        # know how to obtain the CSV.
        #

        return self._client.download_csv(
            config
        )