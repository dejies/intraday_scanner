"""
Market Feed Provider Factory.
"""

from __future__ import annotations

from src.core.config import settings

from src.models.enums import MarketMode

from src.providers.dhan import (
    MarketFeedProvider,
    DhanLiveProvider,
    DhanSandboxProvider,
)

from src.services.watchlist import WatchlistService


class ProviderFactory:
    """
    Factory responsible for creating the configured
    Market Feed provider.
    """

    @staticmethod
    def create(
        watchlist: WatchlistService,
        on_connect,
        on_message,
        on_close,
        on_error,
    ) -> MarketFeedProvider:

        print(f"Market Mode: {settings.market_mode}")

        if settings.market_mode == MarketMode.LIVE:
            print("Creating DhanLiveProvider")

        elif settings.market_mode == MarketMode.SANDBOX:
            print("Creating DhanSandboxProvider")

        if settings.market_mode == MarketMode.LIVE:

            return DhanLiveProvider(
                watchlist=watchlist,
                on_connect=on_connect,
                on_message=on_message,
                on_close=on_close,
                on_error=on_error,
            )

        if settings.market_mode == MarketMode.SANDBOX:

            return DhanSandboxProvider(
                watchlist=watchlist,
                on_connect=on_connect,
                on_message=on_message,
                on_close=on_close,
                on_error=on_error,
            )

        raise RuntimeError(
            f"Unsupported MarketMode: {settings.market_mode}"
        )