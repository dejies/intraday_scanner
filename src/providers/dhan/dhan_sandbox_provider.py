"""
Dhan Sandbox Provider.
"""

from __future__ import annotations

from dhanhq import DhanContext
from dhanhq.marketfeed import MarketFeed

from src.providers.dhan.base_dhan_provider import BaseDhanProvider


class DhanSandboxProvider(BaseDhanProvider):
    """
    Dhan Sandbox Market Feed Provider.
    """

    def _create_context(self) -> DhanContext:

        return DhanContext(
            self.settings.dhan_sandbox_client_id,
            self.settings.dhan_sandbox_access_token,
        )

    def _create_feed(
        self,
        context: DhanContext,
        instruments,
    ) -> MarketFeed:

        #
        # Replace this with the actual Sandbox feed
        # once Dhan exposes the sandbox implementation.
        #
        return MarketFeed(
            dhan_context=context,
            instruments=instruments,
            version="v2",
            on_connect=self._handle_connect,
            on_message=self._on_message,
            on_close=self._handle_close,
            on_error=self._handle_error,
        )