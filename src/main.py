"""
Application Entry Point
"""

from __future__ import annotations

import threading
import time

from PySide6.QtWidgets import QApplication

from src.services.instrument_state_service import InstrumentStateService
from src.services import InstrumentBootstrapService
from src.providers.dhan.provider_factory import ProviderFactory
from src.dashboard.dashboard_window import DashboardWindow
from src.dashboard.dashboard_controller import DashboardController
from src.scanner import Scanner
from src.services.market_data import MarketData
from src.services.historical_data import HistoricalDataService
from src.services.websocket_client import WebSocketClient
from src.core.market_data_store import MarketDataStore
from src.services.gap_service import GapService
from src.services.instrument_master_service import (
    InstrumentMasterService,
)
from src.watchlist import WatchlistService
from src.services.universe.universe_module import UniverseModule
from src.database import SQLiteManager

from src.repositories import (
    CandleRepository,
    IndicatorRepository,
)

from src.builders import CandleBuilder

from src.services import CandleService
from src.services.indicator_service import IndicatorService
from src.services.opening_range_service import OpeningRangeService
from src.watchlist import UniverseMonitor


def main() -> None:
    """
    Application entry point.
    """

    #
    # Shared MarketData
    #
    market_data = MarketData()
    market_store = MarketDataStore()

    sqlite = SQLiteManager(
        "data/intraday_scanner.db"
    )

    #
    # Repositories
    #
    candle_repository = CandleRepository(sqlite)

    indicator_repository = IndicatorRepository(
        sqlite,
    )

    #
    # Builders
    #
    candle_builder = CandleBuilder()

    #
    # Services
    #
    indicator_service = IndicatorService()
    opening_range_service = OpeningRangeService()

    gap_service = GapService(
        candle_repository=candle_repository,
    )

    candle_service = CandleService(
        builder=candle_builder,
        repository=candle_repository,
        indicator_repository=indicator_repository,
        indicator_service=indicator_service,
        market_data_store=market_store,
        opening_range_service=opening_range_service,
        gap_service=gap_service,
    )

    instrument_master = InstrumentMasterService()
    instrument_master.load()

    #
    # Market Universe
    #
    universe = UniverseModule(
        sqlite=sqlite,
        instrument_master_service=instrument_master,
    )

    print()
    print("=" * 70)
    print("Synchronizing Market Universe")
    print("=" * 70)

    universe.sync()
    universe.refresh()

    print(
        "Universe loaded:",
        universe.count(),
        "stocks",
    )

    print("=" * 70)
    print()

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
        universe_provider=universe,
        instrument_master_service=instrument_master,
    )

    print()

    #
    # Start WebSocket.
    #
    websocket = WebSocketClient(
        market_data=market_data,
        market_store=market_store,
        watchlist=watchlist,
        candle_service=candle_service,
    )

    print("Creating provider...")

    provider = ProviderFactory.create(
        watchlist=watchlist,
        on_connect=websocket.on_connect,
        on_message=websocket.on_message,
        on_close=websocket.on_close,
        on_error=websocket.on_error,
    )

    websocket.set_provider(provider)

    websocket_thread = threading.Thread(
        target=websocket.connect,
        daemon=True,
        name="MarketFeed",
    )

    websocket_thread.start()

    #
    # Scanner
    #
    scanner = Scanner(
        market_data=market_data,
        market_store=market_store,
        watchlist=watchlist,
        opening_range_service=opening_range_service,
        gap_service=gap_service,
    )

    #
    # Historical Data
    #
    historical = HistoricalDataService(
        market_data=market_data,
        watchlist=watchlist,
        candle_repository=candle_repository,
        indicator_repository=indicator_repository,
        indicator_service=indicator_service,
        gap_service=gap_service,
        market_data_store=market_store,
    )

    state_service = InstrumentStateService()

    bootstrap_service = InstrumentBootstrapService(
        market_data_store=market_store,
        candle_builder=candle_builder,
        historical_data_service=historical,
        state_service=state_service,
        indicator_service=indicator_service,
        scanner=scanner,  # We'll adjust this in the next step
    )

    universe_monitor = UniverseMonitor(
        watchlist_service=watchlist,
        websocket_client=websocket,
        instrument_master_service=instrument_master,
        bootstrap_service=bootstrap_service,
        state_service=state_service,
    )

    universe_monitor.start()

    app = QApplication([])

    window = DashboardWindow()

    controller = DashboardController(
        window=window,
        market_store=market_store,
    )

    controller.start()

    window.show()

    print()
    print("Scanner started...")
    print()

    try:

        def scanner_loop():

            while True:
                scanner.scan()
                time.sleep(1)

        scanner_thread = threading.Thread(
            target=scanner_loop,
            daemon=True,
            name="Scanner",
        )

        scanner_thread.start()

        app.exec()

    except KeyboardInterrupt:

        print()
        print("Stopping scanner...")

        try:
            websocket.on_close(None)
            universe_monitor.stop()
            universe_monitor.join(timeout=2)
        except Exception:
            pass


if __name__ == "__main__":
    main()