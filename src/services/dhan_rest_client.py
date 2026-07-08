"""
Dhan REST client.

Provides access to the Dhan REST APIs using the generic HttpClient.

Unlike DhanClient, this implementation is fully configurable and
supports switching between Sandbox and Live environments by changing
DHAN_BASE_URL in the .env file.
"""

from __future__ import annotations

from typing import Any

from src.core.exceptions import (
    ConfigurationError,
)

from src.services.base_service import BaseService
from src.services.http_client import HttpClient


class DhanRestClient(BaseService):
    """
    Dhan REST API client.

    Uses the generic HttpClient internally.
    """

    def __init__(self) -> None:

        super().__init__()

        #
        # Validate configuration.
        #
        if not self.settings.dhan_client_id:
            raise ConfigurationError(
                "DHAN_CLIENT_ID is not configured."
            )

        if not self.settings.dhan_access_token:
            raise ConfigurationError(
                "DHAN_ACCESS_TOKEN is not configured."
            )

        self.logger.info(
            "Initializing Dhan REST client..."
        )

        #
        # Generic HTTP client.
        #
        self.http = HttpClient(
            base_url=self.settings.dhan_base_url,
            timeout=self.settings.api_timeout,
            retry_count=self.settings.retry_count,
            retry_delay=self.settings.retry_delay,
        )

        #
        # Authentication headers.
        #
        self.http.set_headers(
            {
                "access-token": self.settings.dhan_access_token,
                "client-id": self.settings.dhan_client_id,
                "Content-Type": "application/json",
            }
        )

        self.logger.info(
            "Dhan REST client initialized."
        )

    # ------------------------------------------------------------------
    # Generic wrappers
    # ------------------------------------------------------------------

    def get(
            self,
            endpoint: str,
            params: dict[str, Any] | None = None,
    ) -> Any:
        """
        Execute a GET request.
        """

        return self.http.get(
            endpoint=endpoint,
            params=params,
        )

    # ------------------------------------------------------------------

    def post(
            self,
            endpoint: str,
            payload: dict[str, Any],
    ) -> Any:
        """
        Execute a POST request.
        """

        return self.http.post(
            endpoint=endpoint,
            payload=payload,
        )

    # ------------------------------------------------------------------

    def put(
            self,
            endpoint: str,
            payload: dict[str, Any],
    ) -> Any:
        """
        Execute a PUT request.
        """

        return self.http.put(
            endpoint=endpoint,
            payload=payload,
        )

    # ------------------------------------------------------------------

    def delete(
            self,
            endpoint: str,
    ) -> Any:
        """
        Execute a DELETE request.
        """

        return self.http.delete(
            endpoint=endpoint,
        )

    # ------------------------------------------------------------------

    def download(
            self,
            endpoint: str,
            destination,
    ) -> None:
        """
        Download a file.
        """

        self.http.download(
            endpoint=endpoint,
            destination=destination,
        )