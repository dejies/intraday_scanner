"""
Dhan Market Feed WebSocket Client
"""

from datetime import datetime

from dhanhq import DhanContext, MarketFeed

from src.models.candle import Candle
from src.services.base_service import BaseService
from src.services.market_data import MarketData
from src.services.watchlist import WatchlistService


class WebSocketClient(BaseService):
    """
    Handles Dhan Market Feed WebSocket connection.
    """

    def __init__(
            self,
            market_data: MarketData | None = None,
    ) -> None:
        super().__init__()

        self._connected = False
        #
        # Watchlist
        #
        self.watchlist = WatchlistService()
        self.watchlist.load()

        #
        # Shared market data store
        #
        #
        # Shared MarketData instance.
        #
        self.market_data = market_data or MarketData()

        #
        # Dhan Context
        #
        self.context = DhanContext(
            self.settings.dhan_client_id,
            self.settings.dhan_access_token,
        )

        self.feed = None

        # ----------------------------------------------------------
        # Working candle for every symbol.
        #
        # Example:
        #
        # {
        #     "INFY": Candle(...),
        #     "RELIANCE": Candle(...)
        # }
        # ----------------------------------------------------------
        self._working_candles: dict[str, Candle] = {}

        # ----------------------------------------------------------
        # Current minute for every symbol.
        #
        # Example:
        #
        # {
        #     "INFY": "09:31",
        #     "RELIANCE": "09:31"
        # }
        # ----------------------------------------------------------
        self._current_minute: dict[str, str] = {}

        self.logger.info(
            "WebSocketClient initialized."
        )

    # ------------------------------------------------------------------
    # Callbacks
    # ------------------------------------------------------------------

    def on_connect(self, feed):
        self._connected = True
        self.logger.info(
            "Connected to Dhan Market Feed."
        )

    def on_close(self, feed):
        self._connected = False
        self.logger.warning(
            "Market Feed connection closed."
        )

    def is_connected(self) -> bool:
        """
        Return current WebSocket connection status.
        """

        return self._connected

    def on_error(self, feed, error):
        self.logger.exception(
            "WebSocket Error: %s",
            error,
        )

    # ------------------------------------------------------------------

    def on_message(self, feed, message):
        """
        Handle decoded market data received from Dhan.

        Current Dhan SDK (v2.x) delivers live market data
        through this callback.
        """

        #
        # Ignore unexpected messages.
        #
        if not isinstance(message, dict):
            return

        #
        # We only process Full Data packets.
        #
        if message.get("type") != "Full Data":
            return

        try:

            security_id = int(
                message["security_id"]
            )

            symbol = self.watchlist.get_symbol(
                security_id
            )

            if symbol is None:
                return

            #
            # Latest traded price
            #
            price = float(
                message["LTP"]
            )

            ltq = int(message["LTQ"])

            #
            # Trade time
            #
            trade_time = datetime.strptime(
                message["LTT"],
                "%H:%M:%S",
            )

            #
            # Attach today's date.
            #
            now = datetime.now()

            trade_time = trade_time.replace(
                year=now.year,
                month=now.month,
                day=now.day,
            )

            minute = trade_time.strftime(
                "%Y-%m-%d %H:%M"
            )

            #
            # Forward the tick.
            #
            self._process_tick(
                symbol=symbol,
                price=price,
                volume=ltq,
                trade_time=trade_time,
                minute=minute,
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

    def _process_tick(
            self,
            symbol: str,
            price: float,
            volume: int,
            trade_time: datetime,
            minute: str,
    ) -> None:
        """
        Process one live market tick.
        """

        #
        # Safety fallback.
        #
        if symbol not in self._working_candles:
            self.logger.warning(
                "No working candle for %s. Creating one.",
                symbol,
            )

            self._start_new_candle(
                symbol=symbol,
                price=price,
                volume=volume,
                trade_time=trade_time,
                minute=minute,
            )

            return

        #
        # First tick for this symbol.
        #
        if symbol not in self._working_candles:
            self._start_new_candle(
                symbol=symbol,
                price=price,
                volume=volume,
                trade_time=trade_time,
                minute=minute,
            )

            return

        #
        # Same minute -> update candle.
        #
        if self._current_minute[symbol] == minute:
            self._update_candle(
                symbol=symbol,
                price=price,
                volume=volume,
            )

            return

        #
        # Minute changed.
        #
        self._finalize_candle(symbol)

        self._start_new_candle(
            symbol=symbol,
            price=price,
            volume=volume,
            trade_time=trade_time,
            minute=minute,
        )

    def _start_new_candle(
            self,
            symbol: str,
            price: float,
            volume: int,
            trade_time: datetime,
            minute: str,
    ) -> None:
        """
        Start a new one-minute candle.
        """

        candle = Candle(
            timestamp=trade_time,
            open=price,
            high=price,
            low=price,
            close=price,
            volume=volume,
        )

        self._working_candles[symbol] = candle

        self._current_minute[symbol] = minute

    def _update_candle(
            self,
            symbol: str,
            price: float,
            volume: int,
    ) -> None:
        """
        Update the current working candle.
        """

        candle = self._working_candles[symbol]

        if price > candle.high:
            candle.high = price

        if price < candle.low:
            candle.low = price

        candle.close = price

        #
        # Version 1:
        # We accumulate the received value.
        #
        candle.volume += volume

    def _finalize_candle(
            self,
            symbol: str,
    ) -> None:
        """
        Store completed candle.
        """

        candle = self._working_candles.get(symbol)

        if candle is None:
            return

        latest = self.market_data.get_latest_candle(
            symbol
        )

        if (
                latest is not None
                and latest.timestamp.replace(
            second=0,
            microsecond=0,
        )
                == candle.timestamp.replace(
            second=0,
            microsecond=0,
        )
        ):

            self.market_data.replace_latest_candle(
                symbol,
                candle,
            )

        else:

            self.market_data.add_candle(
                symbol,
                candle,
            )

        self.logger.info(
            "%s  O:%.2f H:%.2f L:%.2f C:%.2f V:%d",
            symbol,
            candle.open,
            candle.high,
            candle.low,
            candle.close,
            candle.volume,
        )


    def _get_instruments(self):
        """
        Build subscription list.
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

    # ------------------------------------------------------------------

    def connect(self) -> None:
        """
        Connect to Dhan Market Feed.
        """

        self.logger.info("Preparing Market Feed...")

        instruments = self._get_instruments()

        self.logger.info(
            "Subscribing to %d instruments.",
            len(instruments),
        )

        #
        # Continue from historical candles.
        #
        self._initialize_working_candles()

        self.feed = MarketFeed(
            dhan_context=self.context,
            instruments=instruments,
            version="v2",
            on_connect=self.on_connect,
            on_message=self.on_message,
            on_close=self.on_close,
            on_error=self.on_error,
        )

        self.mark_initialized()

        self.feed.start()

        self.logger.info(
            "Market Feed thread started."
        )

    def _initialize_working_candles(self) -> None:
        """
        Initialize working candles from historical data.
        """

        for symbol in self.market_data.get_symbols():

            candle = self.market_data.get_latest_candle(
                symbol
            )

            if candle is None:
                continue

            self._working_candles[symbol] = Candle(
                timestamp=candle.timestamp,
                open=candle.open,
                high=candle.high,
                low=candle.low,
                close=candle.close,
                volume=candle.volume,
            )

            self._current_minute[symbol] = (
                candle.timestamp.strftime(
                    "%Y-%m-%d %H:%M"
                )
            )

        self.logger.info(
            "Initialized %d working candles.",
            len(self._working_candles),
        )