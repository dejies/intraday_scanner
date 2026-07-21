"""
Base implementation for Dhan Market Feed providers.
"""

from __future__ import annotations

from abc import abstractmethod
from typing import Callable

from dhanhq import MarketFeed

from src.services.base_service import BaseService
from src.watchlist import WatchlistService
from src.providers.dhan.market_feed_provider import (
    MarketFeedProvider,
)


class BaseDhanProvider(
    BaseService,
    MarketFeedProvider,
):
    """
    Base class shared by all Dhan providers.

    Responsibilities
    ----------------
    - Build subscription list
    - Manage connection state
    - Start/Stop MarketFeed
    - Wrap SDK callbacks

    Subclasses only create the Context and MarketFeed.
    """

    def __init__(
        self,
        watchlist: WatchlistService,
        on_connect: Callable,
        on_message: Callable,
        on_close: Callable,
        on_error: Callable,
    ) -> None:

        super().__init__()

        self.watchlist = watchlist

        self._connected = False

        self._on_connect = on_connect
        self._on_message = on_message
        self._on_close = on_close
        self._on_error = on_error

        self.context = None
        self.feed = None

    # ------------------------------------------------------------------
    # Abstract methods
    # ------------------------------------------------------------------

    @abstractmethod
    def _create_context(self):
        """
        Create the provider-specific DhanContext.
        """
        raise NotImplementedError

    @abstractmethod
    def _create_feed(
            self,
            context,
            instruments: list[tuple],
    ):
        """
        Create the provider-specific MarketFeed instance.
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Common implementation
    # ------------------------------------------------------------------

    def _build_subscription(self) -> list[tuple]:
        """
        Build MarketFeed subscription list.
        """

        instruments = []

        for instrument in self.watchlist.get_all():

            instruments.append(
                (
                    MarketFeed.NSE,
                    str(instrument.security_id),
                    MarketFeed.Full,
                )
            )

        return instruments

    # ------------------------------------------------------------------

    def connect(self) -> None:
        """
        Prepare the provider.
        """

        self.logger.info(
            "Preparing Market Feed..."
        )

        instruments = self._build_subscription()

        self.logger.info(
            "Subscribing to %d instruments.",
            len(instruments),
        )

        self.context = self._create_context()

        self.feed = self._create_feed(
            self.context,
            instruments
        )

        self.mark_initialized()

    # ------------------------------------------------------------------

    def start(self) -> None:
        """
        Start MarketFeed.
        """

        if self.feed is None:
            raise RuntimeError(
                "connect() must be called before start()."
            )

        self.feed.start()

        self.logger.info(
            "Market Feed thread started."
        )

    # ------------------------------------------------------------------

    def stop(self) -> None:
        """
        Stop MarketFeed.
        """

        if self.feed is not None:

            try:
                self.feed.disconnect()
            except Exception:
                pass

        self._connected = False

    # ------------------------------------------------------------------

    def is_connected(self) -> bool:

        return self._connected

    # ------------------------------------------------------------------
    # Callback wrappers
    # ------------------------------------------------------------------

    def _handle_connect(self, feed):

        self._connected = True

        self._on_connect(feed)

    # ------------------------------------------------------------------

    def _handle_close(self, feed):

        self._connected = False

        self._on_close(feed)

    # ------------------------------------------------------------------

    def _handle_error(
        self,
        feed,
        error,
    ):

        self._connected = False

        self._on_error(
            feed,
            error,
        )

    def subscribe_symbols(
            self,
            subscriptions: list[tuple],
    ) -> None:
        """
        Subscribe additional instruments while connected.
        """

        if not subscriptions:
            return

        if self.feed is None:
            raise RuntimeError("MarketFeed is not initialized.")

        self.logger.info(
            "Subscribing %d instruments.",
            len(subscriptions),
        )

        self.feed.subscribe_symbols(subscriptions)

    def unsubscribe_symbols(
            self,
            subscriptions: list[tuple],
    ) -> None:
        """
        Unsubscribe instruments while connected.
        """

        if not subscriptions:
            return

        if self.feed is None:
            raise RuntimeError("MarketFeed is not initialized.")

        self.logger.info(
            "Unsubscribing %d instruments.",
            len(subscriptions),
        )

        self.feed.unsubscribe_symbols(subscriptions)