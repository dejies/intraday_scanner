"""
Base service class.

Provides common functionality shared by all services.
"""

from __future__ import annotations

from src.core.config import settings
from src.core.logger import get_logger


class BaseService:
    """
    Base class for all services.

    Every service gets:
        - Logger
        - Application settings
    """

    def __init__(self) -> None:
        self.logger = get_logger(self.__class__.__name__)
        self.settings = settings