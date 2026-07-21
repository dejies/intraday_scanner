"""
Live Dhan Market Feed Provider.
"""

from __future__ import annotations

from typing import Callable

from dhanhq import DhanContext, MarketFeed

from src.services.watchlist import WatchlistService


from src.providers.dhan.base_dhan_provider import BaseDhanProvider

class DhanLiveProvider(BaseDhanProvider):

    """
    Encapsulates the Dhan Live MarketFeed SDK.

    Responsibilities
    ----------------
    - Create DhanContext
    - Create MarketFeed
    - Subscribe to instruments
    - Start/Stop the feed

    Must NOT
    --------
    - Process ticks
    - Build candles
    - Calculate indicators
    - Generate signals
    """

    
    def _create_feed(
        self,
        context,
        instruments: list[tuple],
    ) -> MarketFeed:
        """
        Create the Dhan Live MarketFeed.
        """

        return MarketFeed(
            dhan_context=context,
            instruments=instruments,
            version="v2",
            on_connect=self._handle_connect,
            on_message=self._on_message,
            on_close=self._handle_close,
            on_error=self._handle_error,
        )

    def _create_context(self) -> DhanContext:
        """
        Create the Dhan Live context.
        """

        return DhanContext(
            self.settings.dhan_client_id,
            self.settings.dhan_access_token,
        )