from __future__ import annotations

from src.database.universe_repository import UniverseRepository

from src.services.universe.clients import NSEHttpClient
from src.services.universe.clients.nse_download_service import (
    NSEDownloadService,
)
from src.services.universe.config import (
    MIDCAP150,
    NIFTY500,
    SMALLCAP250,
)
from src.services.universe.providers.nse_index_provider import (
    NSEIndexProvider,
)
from src.services.universe.universe_manager import UniverseManager
from src.services.universe.universe_sync_service import (
    UniverseSyncService,
)


class UniverseModule:
    """
    Wires together the complete Market Universe subsystem.
    """

    def __init__(
        self,
        sqlite,
        instrument_master_service,
    ):

        #
        # Repository
        #
        repository = UniverseRepository(sqlite)

        #
        # HTTP Client
        #
        client = NSEHttpClient()
        client.initialize()

        downloader = NSEDownloadService(client)

        #
        # Providers
        #
        providers = [
            NSEIndexProvider(
                downloader,
                NIFTY500,
            ),
            NSEIndexProvider(
                downloader,
                MIDCAP150,
            ),
            NSEIndexProvider(
                downloader,
                SMALLCAP250,
            ),
        ]

        #
        # Public objects
        #
        self.manager = UniverseManager(
            repository,
        )

        self.sync_service = UniverseSyncService(
            sqlite=sqlite,
            repository=repository,
            providers=providers,
            instrument_master_service=instrument_master_service,
        )

    # ---------------------------------------------------------

    def sync(self):
        """
        Synchronize the market universe.
        """
        self.sync_service.sync()

    # ---------------------------------------------------------

    def refresh(self):
        """
        Reload the cached universe from SQLite.
        """
        self.manager.refresh()

    # ---------------------------------------------------------

    def symbols(self):
        return self.get_symbols()

    def get_symbols(self) -> set[str]:
        return self.manager.symbols()

    # ---------------------------------------------------------

    def stocks(self):
        return self.manager.stocks()

    # ---------------------------------------------------------

    def count(self):
        return self.manager.count()

    # ---------------------------------------------------------

    def get(self, symbol: str):
        return self.manager.get(symbol)

    # ---------------------------------------------------------

    def contains(self, symbol: str):
        return self.manager.contains(symbol)