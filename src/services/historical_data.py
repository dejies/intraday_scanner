"""
Historical Data Service

Downloads historical market candles from Dhan and
loads them into the shared MarketData store.
"""

from __future__ import annotations

from datetime import datetime, timedelta

from dhanhq import DhanContext, dhanhq

from src.core.constants import Exchange
from src.models.candle import Candle
from src.models.stock import Stock
from src.services.base_service import BaseService
from src.services.market_data import MarketData
from src.services.watchlist import WatchlistService
import time

class HistoricalDataService(BaseService):
    """
    Loads historical candles from Dhan.
    """

    def __init__(
            self,
            market_data: MarketData,
    ) -> None:
        super().__init__()

        self.market_data = market_data

        #
        # Watchlist
        #
        self.watchlist = WatchlistService()
        self.watchlist.load()

        #
        # Shared Dhan Context
        #
        self.context = DhanContext(
            self.settings.dhan_client_id,
            self.settings.dhan_access_token,
        )

        #
        # Dhan REST Client
        #
        self.dhan = dhanhq(
            self.context,
        )

        self.logger.info(
            "HistoricalDataService initialized."
        )

    # ------------------------------------------------------------------

    def load(self) -> None:
        """
        Load historical data for all enabled stocks.
        """

        self.logger.info(
            "Loading historical candles..."
        )

        for stock in self.watchlist.get_all():

            try:

                self._load_symbol(stock)

                #
                # Respect Dhan rate limits.
                #
                time.sleep(0.5)

            except Exception:

                self.logger.exception(
                    "Unable to load history for %s",
                    stock.symbol,
                )

        self.logger.info(
            "Historical loading completed."
        )

    # ------------------------------------------------------------------

    def _load_symbol(
            self,
            stock: Stock,
    ) -> None:
        """
        Load historical candles for one stock.

        Retries automatically if Dhan rate-limits
        the request (DH-904).
        """

        max_retries = 3

        for attempt in range(1, max_retries + 1):

            response = self._download_history(stock)

            #
            # Success?
            #
            if response.get("status") == "success":

                candles = self._convert_to_candles(
                    response,
                )

                if candles:
                    self.market_data.add_candles(
                        stock.symbol,
                        candles,
                    )

                    self.logger.info(
                        "%s : Loaded %d historical candles.",
                        stock.symbol,
                        len(candles),
                    )

                    return

                #
                # Successful response but no data.
                #
                self.logger.warning(
                    "No historical candles for %s",
                    stock.symbol,
                )

                return

            #
            # Failed request
            #
            remarks = response.get("remarks", {})

            error_code = ""

            if isinstance(remarks, dict):
                error_code = remarks.get(
                    "error_code",
                    "",
                )

            #
            # Retry only for rate limit.
            #
            if (
                    error_code == "DH-904"
                    and attempt < max_retries
            ):
                self.logger.warning(
                    "%s : Rate limited. Retry %d/%d...",
                    stock.symbol,
                    attempt,
                    max_retries,
                )

                time.sleep(1)

                continue

            #
            # Final failure.
            #
            self.logger.error(
                "%s : Historical download failed: %s",
                stock.symbol,
                response,
            )

            return

    # ------------------------------------------------------------------

    def _download_history(
            self,
            stock: Stock,
    ):
        """
        Download historical candles.

        Strategy:
            1. Load today's candles.
            2. If insufficient, load yesterday.
        """

        today = datetime.now().date()

        response = self.dhan.intraday_minute_data(
            security_id=str(stock.security_id),
            exchange_segment=self.dhan.NSE,
            instrument_type="EQUITY",
            from_date=today.strftime("%Y-%m-%d"),
            to_date=today.strftime("%Y-%m-%d"),
            interval=1,
        )

        data = response.get("data")

        if not data:
            return response

        #
        # Enough candles?
        #
        if len(data["close"]) >= self.settings.max_candles:
            return response

        #
        # Need previous day.
        #
        previous = today - timedelta(days=1)

        previous_response = self.dhan.intraday_minute_data(
            security_id=str(stock.security_id),
            exchange_segment=self.dhan.NSE,
            instrument_type="EQUITY",
            from_date=previous.strftime("%Y-%m-%d"),
            to_date=previous.strftime("%Y-%m-%d"),
            interval=1,
        )

        previous_data = previous_response.get("data")

        if not previous_data:
            return response

        #
        # Merge all arrays.
        #
        merged = {}

        for key in data.keys():
            merged[key] = previous_data[key] + data[key]

        response["data"] = merged

        return response

    # ------------------------------------------------------------------

    def _convert_to_candles(
            self,
            response,
    ) -> list[Candle]:
        """
        Convert Dhan response into Candle objects.
        """

        data = response.get("data")

        if not data:
            return []

        opens = data["open"]
        highs = data["high"]
        lows = data["low"]
        closes = data["close"]
        volumes = data["volume"]
        timestamps = data["timestamp"]

        #
        # Keep only latest candles.
        #
        max_candles = self.settings.max_candles

        start = max(
            0,
            len(opens) - max_candles,
        )

        candles = []

        for i in range(start, len(opens)):
            candles.append(
                Candle(
                    timestamp=datetime.fromtimestamp(
                        timestamps[i]
                    ),
                    open=float(opens[i]),
                    high=float(highs[i]),
                    low=float(lows[i]),
                    close=float(closes[i]),
                    volume=int(volumes[i]),
                )
            )

        return candles