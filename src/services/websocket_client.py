"""
Dhan Market Feed WebSocket Client
"""

from dhanhq import DhanContext, MarketFeed

from src.providers.dhan.market_feed_provider import MarketFeedProvider
from src.services.candle_service import CandleService
from src.services.base_service import BaseService
from src.services.market_data import MarketData
from src.services.watchlist import WatchlistService
from src.providers.dhan.tick_processor import TickProcessor
from src.core.market_data_store import MarketDataStore
from src.models.enums import ConnectionState
from datetime import datetime, time
from src.models.enums import MarketState


class WebSocketClient(BaseService):
    """
    Handles Dhan Market Feed WebSocket connection.
    """

    def __init__(
            self,
            market_data: MarketData,
            market_store: MarketDataStore,
            watchlist: WatchlistService,
            candle_service: CandleService,
    ) -> None:
        super().__init__()

        self._connected = False
        #
        # Watchlist
        #
        self.watchlist = watchlist

        self.tick_processor = TickProcessor(
            self.watchlist
        )
        #
        # Shared market data store
        #
        #
        # Shared MarketData instance.
        #
        self.market_data = market_data or MarketData()

        self.market_store = market_store

        self.candle_service = candle_service

        self.provider: MarketFeedProvider | None = None

        self.logger.info(
            "WebSocketClient initialized."
        )

    # ------------------------------------------------------------------
    # Callbacks
    # ------------------------------------------------------------------

    def on_connect(self, feed):
        """
        Called when the WebSocket connection is established.
        """

        self._connected = True

        self.market_store.update_market_status(
            lambda status: setattr(
                status,
                "connection_state",
                ConnectionState.CONNECTED,
            )
        )

        self.logger.info(
            "Connected to Dhan Market Feed."
        )

    def on_close(self, feed):
        """
        Called when the WebSocket connection is closed.
        """

        self._connected = False

        self.market_store.update_market_status(
            lambda status: setattr(
                status,
                "connection_state",
                ConnectionState.DISCONNECTED,
            )
        )

        self.logger.warning(
            "Market Feed connection closed."
        )

    def is_connected(self) -> bool:
        """
        Return current WebSocket connection status.
        """

        return self._connected

    def on_error(self, feed, error):
        """
        Called when a WebSocket error occurs.
        """

        self.market_store.update_market_status(
            lambda status: setattr(
                status,
                "connection_state",
                ConnectionState.DISCONNECTED,
            )
        )

        self.logger.exception(
            "WebSocket Error: %s",
            error,
        )

    # ------------------------------------------------------------------

    def on_message(self, feed, message):
        """
        Handle decoded market data received from Dhan.
        """

        try:

            #
            # Convert Dhan message to our Tick model.
            #

            self._update_market_state()

            tick = self.tick_processor.process(message)

            if tick is None:
                print(f"Tick received: {tick.security_id}")
                return

            self._update_market_state()

            self.market_store.update_tick(tick)

            result = self.candle_service.process_tick(tick)

            self.market_store.update_candle(
                tick.security_id,
                result.current_candle,
            )


        except Exception:

            self.logger.exception(
                "Unable to process market message."
            )

    # ------------------------------------------------------------------

    def on_ticks(self, feed, ticks):
        """
        Not used.

        Current Dhan SDK delivers decoded ticks
        through on_message().
        """
        pass

    # ------------------------------------------------------------------



    def _get_instruments(self):
        """
        Build subscription list.
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

    # ------------------------------------------------------------------

    def connect(self) -> None:
        """
        Connect to the configured Market Feed provider.
        """

        if self.provider is None:
            raise RuntimeError(
                "MarketFeedProvider has not been configured."
            )

        self.logger.info(
            "Preparing Market Feed..."
        )

        self.provider.connect()

        self.mark_initialized()

        self.provider.start()

        self.logger.info(
            "Market Feed thread started."
        )


    def _update_market_state(self) -> None:
        """
        Update the current market state.
        """

        now = datetime.now().time()

        if time(9, 15) <= now <= time(15, 30):
            state = MarketState.OPEN
        else:
            state = MarketState.CLOSED

        self.market_store.update_market_status(
            lambda status: setattr(
                status,
                "market_state",
                state,
            )
        )

    def set_provider(
            self,
            provider: MarketFeedProvider,
    ) -> None:

        self.provider = provider

    def update_watchlist(
            self,
            added: list[tuple],
            removed: list[tuple],
    ):

        if added:
            self.provider.subscribe_symbols(added)

        if removed:
            self.provider.unsubscribe_symbols(removed)