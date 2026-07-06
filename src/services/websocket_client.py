"""
Dhan Market Feed WebSocket Client
"""

from __future__ import annotations

from dhanhq import DhanContext, MarketFeed

from src.services.base_service import BaseService
from src.services.watchlist import WatchlistService


class WebSocketClient(BaseService):
    """
    Handles Dhan Market Feed WebSocket connection.
    """

    def __init__(self) -> None:
        super().__init__()

        self.watchlist = WatchlistService()
        self.watchlist.load()

        self.context = DhanContext(
            self.settings.dhan_client_id,
            self.settings.dhan_access_token,
        )

        self.feed = None

    # ------------------------------------------------------------------
    # Callbacks
    # ------------------------------------------------------------------

    def on_connect(self, feed):
        self.logger.info("Connected to Dhan Market Feed.")

    def on_close(self, feed):
        self.logger.warning("Market Feed connection closed.")

    def on_error(self, feed, error):
        self.logger.exception("WebSocket Error: %s", error)

    def on_message(self, feed, message):
        self.logger.debug("Message: %s", message)

    def on_ticks(self, feed, ticks):
        self.logger.info("Tick: %s", ticks)

    # ------------------------------------------------------------------

    def _get_instruments(self):
        """
        Build instrument subscription list.
        """

        instruments = []

        for stock in self.watchlist.get_all():

            instruments.append(
                (
                    MarketFeed.NSE,
                    str(stock.security_id),
                    MarketFeed.Full,
                )
            )

        return instruments

    # ------------------------------------------------------------------

    def connect(self):
        """
        Connect to Dhan Market Feed.
        """

        self.logger.info("Preparing Market Feed...")

        instruments = self._get_instruments()

        self.logger.info(
            "Subscribing to %d instruments.",
            len(instruments),
        )

        self.feed = MarketFeed(
            dhan_context=self.context,
            instruments=instruments,
            version="v2",
            on_connect=self.on_connect,
            on_message=self.on_message,
            on_close=self.on_close,
            on_error=self.on_error,
            on_ticks=self.on_ticks,
        )

        self.mark_initialized()

        try:

            self.feed.run()

        except KeyboardInterrupt:

            self.logger.info(
                "Stopping WebSocket..."
            )

        except Exception:

            self.logger.exception(
                "Unexpected WebSocket error."
            )

        finally:

            if self.feed is not None:

                try:
                    self.feed.close_connection()
                except Exception:
                    pass