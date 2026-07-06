"""
Custom application exceptions.
"""


class ScannerException(Exception):
    """Base exception for all application exceptions."""


class ConfigurationError(ScannerException):
    """Raised when application configuration is invalid."""


class WatchlistError(ScannerException):
    """Raised when the watchlist is invalid."""


class DhanConnectionError(ScannerException):
    """Raised when Dhan API connection fails."""


class WebSocketError(ScannerException):
    """Raised when WebSocket connection fails."""