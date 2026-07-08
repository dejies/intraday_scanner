"""
Dhan API client.

Encapsulates all interactions with the Dhan SDK.
"""

from __future__ import annotations

from typing import Any

from dhanhq import dhanhq

from src.core.exceptions import (
    ConfigurationError,
    DhanConnectionError,
)

from src.services.base_service import BaseService


class DhanClient(BaseService):
    """
    Wrapper around the Dhan SDK.

    NOTE
    ----
    This class currently uses the official Dhan SDK.

    The SDK internally connects to the production API.

    In a future phase this wrapper will migrate to a
    configurable REST implementation while keeping the
    public interface unchanged.
    """

    def __init__(self) -> None:

        super().__init__()

        #
        # Validate configuration
        #
        if not self.settings.dhan_client_id:
            raise ConfigurationError(
                "DHAN_CLIENT_ID is not configured."
            )

        if not self.settings.dhan_access_token:
            raise ConfigurationError(
                "DHAN_ACCESS_TOKEN is not configured."
            )

        #
        # Save configuration.
        #
        self.client_id = self.settings.dhan_client_id

        self.access_token = self.settings.dhan_access_token

        #
        # Reserved for REST migration.
        #
        self.base_url = self.settings.dhan_base_url

        self.market_feed_url = (
            self.settings.dhan_market_feed_url
        )

        self.timeout = self.settings.api_timeout

        self.logger.info(
            "Initializing Dhan client..."
        )

        self.logger.info(
            "Base URL : %s",
            self.base_url,
        )

        #
        # SDK initialization.
        #
        self._client = dhanhq(
            self.client_id,
            self.access_token,
        )

        self.logger.info(
            "Dhan client created."
        )

    # ------------------------------------------------------------------

    @property
    def client(self) -> dhanhq:
        """
        Return the underlying SDK instance.
        """

        return self._client

    # ------------------------------------------------------------------

    @property
    def connected(self) -> bool:
        """
        Returns True if the client has been successfully verified.
        """

        return self.initialized

    # ------------------------------------------------------------------

    def verify_connection(self) -> bool:
        """
        Verify connectivity.

        Raises
        ------
        DhanConnectionError
        """

        self.logger.info(
            "Verifying Dhan connection..."
        )

        try:

            self.get_fund_limits()

            self._initialized = True

            self.logger.info(
                "Successfully connected to Dhan."
            )

            return True

        except Exception as exc:

            self.logger.exception(
                "Failed to connect to Dhan."
            )

            raise DhanConnectionError(
                f"Unable to connect to Dhan: {exc}"
            ) from exc

    # ------------------------------------------------------------------

    def get_fund_limits(
        self,
    ) -> dict[str, Any]:
        """
        Return account fund limits.
        """

        self.logger.debug(
            "Fetching fund limits."
        )

        return self._client.get_fund_limits()

    # ------------------------------------------------------------------

    def get_orders(
        self,
    ) -> dict[str, Any]:
        """
        Return order book.
        """

        self.logger.debug(
            "Fetching orders."
        )

        return self._client.get_order_list()

    # ------------------------------------------------------------------

    def get_holdings(
        self,
    ) -> dict[str, Any]:
        """
        Return holdings.
        """

        self.logger.debug(
            "Fetching holdings."
        )

        return self._client.get_holdings()

    # ------------------------------------------------------------------

    def get_positions(
        self,
    ) -> dict[str, Any]:
        """
        Return positions.
        """

        self.logger.debug(
            "Fetching positions."
        )

        return self._client.get_positions()

    # ------------------------------------------------------------------

    def get_trades(
        self,
    ) -> dict[str, Any]:
        """
        Return trade book.
        """

        self.logger.debug(
            "Fetching trades."
        )

        return self._client.get_trade_book()