"""
Base service class.
"""

from src.core.config import settings
from src.core.logger import get_logger


class BaseService:
    """
    Base class for all services.
    """

    def __init__(self) -> None:
        self.settings = settings
        self.logger = get_logger(self.__class__.__name__)
        self._initialized = False

    @property
    def initialized(self) -> bool:
        return self._initialized

    def mark_initialized(self) -> None:
        self._initialized = True

    def mark_uninitialized(self) -> None:
        self._initialized = False