"""
Historical Data Service

Downloads historical market candles from Dhan and
loads them into the shared MarketData store.
"""

from __future__ import annotations

from datetime import datetime
from datetime import timedelta
import time

from dhanhq import DhanContext
from dhanhq import dhanhq

from src.models.candle import Candle
from src.models.instrument import Instrument

from src.services.base_service import BaseService
from src.services.market_data import MarketData
from src.services.watchlist import WatchlistService


class HistoricalDataService(BaseService):
    """
    Downloads historical candles for all instruments in the
    watchlist and stores them in the shared MarketData object.
    """

    def __init__(
            self,
            market_data: MarketData,
            watchlist: WatchlistService,
    ) -> None:

        super().__init__()

        #
        # Shared MarketData.
        #
        self.market_data = market_data

        #
        # Shared Watchlist.
        #
        self.watchlist = watchlist

        #
        # Shared Dhan Context.
        #
        self.context = DhanContext(
            self.settings.dhan_client_id,
            self.settings.dhan_access_token,
        )

        #
        # REST client.
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
        Load historical candles for every enabled instrument.
        """

        self.logger.info(
            "Loading historical candles..."
        )

        instruments = self.watchlist.get_all()

        self.logger.info(
            "Loading history for %d instruments.",
            len(instruments),
        )

        for instrument in instruments:

            try:

                self._load_symbol(
                    instrument,
                )

                #
                # Respect Dhan rate limits.
                #
                time.sleep(
                    self.settings.retry_delay
                )

            except Exception:

                self.logger.exception(
                    "Unable to load history for %s",
                    instrument.symbol,
                )

        self.logger.info(
            "Historical loading completed."
        )

    # ------------------------------------------------------------------

    def _load_symbol(
            self,
            instrument: Instrument,
    ) -> None:
        """
        Download historical candles for a single instrument.

        Automatically retries on temporary API failures.
        """

        max_retries = self.settings.retry_count

        for attempt in range(
                1,
                max_retries + 1,
        ):

            response = self._download_history(
                instrument,
            )

            #
            # Success.
            #
            if response.get(
                    "status"
            ) == "success":

                candles = self._convert_to_candles(
                    response,
                )

                if candles:

                    self.market_data.add_candles(
                        instrument.symbol,
                        candles,
                    )

                    self.logger.info(
                        "%s : Loaded %d candles.",
                        instrument.symbol,
                        len(candles),
                    )

                    return

                self.logger.warning(
                    "%s : No historical candles returned.",
                    instrument.symbol,
                )

                return

            #
            # Error response.
            #
            remarks = response.get(
                "remarks",
                {},
            )

            error_code = ""

            if isinstance(
                    remarks,
                    dict,
            ):
                error_code = remarks.get(
                    "error_code",
                    "",
                )

            #
            # Retry only on rate limiting.
            #
            if (
                    error_code == "DH-904"
                    and attempt < max_retries
            ):

                self.logger.warning(
                    "%s : Rate limited "
                    "(%d/%d). Retrying...",
                    instrument.symbol,
                    attempt,
                    max_retries,
                )

                time.sleep(
                    self.settings.retry_delay
                )

                continue

            #
            # Permanent failure.
            #
            self.logger.error(
                "%s : Failed to download "
                "historical data.",
                instrument.symbol,
            )

            self.logger.error(
                "%s : %s",
                instrument.symbol,
                response,
            )

            return

    # ------------------------------------------------------------------

    # ------------------------------------------------------------------

    def _download_history(
            self,
            instrument: Instrument,
    ):
        """
        Download historical candles.

        Strategy
        --------
        Walk backwards for N days until enough candles
        are collected.
        """

        today = datetime.now().date()

        exchange_segment = self._get_exchange_segment(
            instrument,
        )

        instrument_type = self._get_instrument_type(
            instrument,
        )

        merged = None

        #
        # Walk backwards through the configured number
        # of days.
        #
        for i in range(
                self.settings.historical_lookback_days
        ):

            day = today - timedelta(days=i)

            response = self.dhan.intraday_minute_data(
                security_id=str(
                    instrument.security_id
                ),
                exchange_segment=exchange_segment,
                instrument_type=instrument_type,
                from_date=day.strftime("%Y-%m-%d"),
                to_date=day.strftime("%Y-%m-%d"),
                interval=self.settings.historical_interval,
            )

            #
            # API failure.
            #
            if response.get("status") != "success":
                return response

            data = response.get("data")

            #
            # Weekend / holiday.
            #
            if not data:
                continue

            #
            # First successful day.
            #
            if merged is None:

                merged = data

            else:

                #
                # Older candles should appear before
                # newer candles.
                #
                for key in merged.keys():
                    merged[key] = (
                            data[key]
                            + merged[key]
                    )

            #
            # Enough candles collected?
            #
            if (
                    len(merged["close"])
                    >= self.settings.max_candles
            ):
                break

        #
        # Nothing downloaded.
        #
        if merged is None:
            return {
                "status": "success",
                "data": None,
            }

        #
        # Trim to max candles.
        #
        start = max(
            0,
            len(merged["close"])
            - self.settings.max_candles,
        )

        for key in merged.keys():
            merged[key] = merged[key][start:]

        return {
            "status": "success",
            "data": merged,
        }

    # ------------------------------------------------------------------

    def _get_exchange_segment(
            self,
            instrument: Instrument,
    ):
        """
        Convert Instrument exchange into the Dhan SDK
        exchange segment.
        """

        exchange = instrument.exchange.upper()

        if exchange == "NSE":
            return self.dhan.NSE

        if exchange == "BSE":
            return self.dhan.BSE

        #
        # Future exchanges can be added here.
        #
        raise ValueError(
            f"Unsupported exchange: {exchange}"
        )

    # ------------------------------------------------------------------

    def _get_instrument_type(
            self,
            instrument: Instrument,
    ) -> str:
        """
        Convert Instrument type into Dhan API value.
        """

        instrument_type = (
            instrument.instrument_type.upper()
        )

        #
        # Equity
        #
        if (
                "EQUITY" in instrument_type
                or instrument.segment == "E"
        ):
            return "EQUITY"

        #
        # Futures
        #
        if (
                "FUTURE" in instrument_type
                or instrument.segment == "D"
        ):
            return "FUTIDX"

        #
        # Options
        #
        if (
                "OPTION" in instrument_type
        ):
            return "OPTIDX"

        #
        # Default.
        #
        return "EQUITY"

    # ------------------------------------------------------------------

    # ------------------------------------------------------------------

    def _convert_to_candles(
            self,
            response: dict,
    ) -> list[Candle]:
        """
        Convert Dhan historical response into Candle objects.
        """

        data = response.get("data")

        if not data:
            return []

        required_fields = (
            "open",
            "high",
            "low",
            "close",
            "volume",
            "timestamp",
        )

        #
        # Validate response.
        #
        for field in required_fields:

            if field not in data:
                self.logger.warning(
                    "Historical response missing field '%s'.",
                    field,
                )

                return []

        opens = data["open"]
        highs = data["high"]
        lows = data["low"]
        closes = data["close"]
        volumes = data["volume"]
        timestamps = data["timestamp"]

        #
        # Validate array lengths.
        #
        length = len(opens)

        if not all(
                len(values) == length
                for values in (
                        highs,
                        lows,
                        closes,
                        volumes,
                        timestamps,
                )
        ):
            self.logger.error(
                "Historical response contains inconsistent array lengths."
            )

            return []

        #
        # Keep only latest candles.
        #
        start = max(
            0,
            length - self.settings.max_candles,
        )

        candles: list[Candle] = []

        for index in range(start, length):

            try:

                candles.append(

                    Candle(

                        timestamp=datetime.fromtimestamp(
                            timestamps[index]
                        ),

                        open=float(opens[index]),

                        high=float(highs[index]),

                        low=float(lows[index]),

                        close=float(closes[index]),

                        volume=int(volumes[index]),
                    )
                )

            except Exception as exc:

                self.logger.warning(
                    "Skipping malformed candle (%d): %s",
                    index,
                    exc,
                )

        return candles