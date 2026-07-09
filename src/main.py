"""
Application Entry Point
"""

from __future__ import annotations

import threading
import time

from src.dashboard import Dashboard
from src.scanner import Scanner
from src.ranking import SignalRanking
from src.services.market_data import MarketData
from src.services.historical_data import HistoricalDataService
from src.services.websocket_client import WebSocketClient
from src.services.watchlist import WatchlistService
from src.services.instrument_master_service import (
    InstrumentMasterService,
)

def main() -> None:
    """
    Application entry point.
    """

    #
    # Shared MarketData
    #
    market_data = MarketData()
    instrument_master = InstrumentMasterService()
    instrument_master.load()
    print()

    print("=" * 70)
    print("Instrument Master")
    print("=" * 70)

    print(
        "Loaded:",
        len(instrument_master.get_all()),
        "instruments",
    )

    print("=" * 70)
    print()

    watchlist = WatchlistService(
        instrument_master=instrument_master,
    )

    watchlist.load()
    #
    # Load historical candles.
    #
    historical = HistoricalDataService(
        market_data=market_data,
        watchlist=watchlist,
    )

    historical.load()

    print()

    print("Historical data loaded")

    #
    # Start WebSocket.
    #
    websocket = WebSocketClient(
        market_data=market_data,
        watchlist=watchlist,
    )

    websocket_thread = threading.Thread(
        target=websocket.connect,
        daemon=True,
        name="MarketFeed",
    )

    websocket_thread.start()

    #
    # Scanner components
    #
    scanner = Scanner(
        market_data=market_data,
    )

    ranking = SignalRanking()

    dashboard = Dashboard()

    print()
    print("Scanner started...")
    print()

    try:

        while True:

            signals = scanner.scan()

            ranked = ranking.rank(
                signals,
            )

            dashboard.display(
                ranked,
                scanner.get_latest_indicators(),
                connected=websocket.is_connected(),
            )

            time.sleep(1)

    except KeyboardInterrupt:

        print()
        print("Stopping scanner...")

        try:
            websocket.on_close(None)
        except Exception:
            pass


if __name__ == "__main__":
    main()