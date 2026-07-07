"""
Intraday Scanner - Main Entry Point
"""

from __future__ import annotations

import time

from src.dashboard import Dashboard
from src.ranking import SignalRanking
from src.scanner import Scanner

from src.services.market_data import MarketData
from src.services.websocket_client import WebSocketClient


def main():

    #
    # Shared market data.
    #
    market_data = MarketData()

    #
    # Core components.
    #
    scanner = Scanner(market_data)

    ranking = SignalRanking()

    dashboard = Dashboard()

    websocket = WebSocketClient(
        market_data=market_data,
    )

    #
    # Start websocket.
    #
    websocket.connect()

    print("\nScanner started...\n")

    try:

        while True:

            signals = scanner.scan()

            signals = ranking.rank(signals)

            dashboard.display(signals)
            for symbol in market_data.get_symbols():
                print(
                    symbol,
                    market_data.get_candle_count(symbol),
                )
            time.sleep(1)


    except KeyboardInterrupt:

        print("\nStopping scanner...")

        if websocket.feed is not None:
            websocket.feed.close_connection()


if __name__ == "__main__":
    main()