"""
Creates the authenticated Dhan context.
"""

from dhanhq import DhanContext

from src.core.exceptions import (
    ConfigurationError,
    DhanConnectionError,
)
from src.services.base_service import BaseService


class DhanContextService(BaseService):

    def __init__(self) -> None:
        super().__init__()

        if not self.settings.dhan_client_id:
            raise ConfigurationError("DHAN_CLIENT_ID is missing.")

        if not self.settings.dhan_access_token:
            raise ConfigurationError("DHAN_ACCESS_TOKEN is missing.")

        self.logger.info("Creating DhanContext...")

        try:
            self._context = DhanContext(
                self.settings.dhan_client_id,
                self.settings.dhan_access_token,
            )

            self.mark_initialized()

            self.logger.info("DhanContext created successfully.")

        except Exception as exc:
            raise DhanConnectionError(str(exc)) from exc

    @property
    def context(self):
        return self._context