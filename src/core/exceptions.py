class ScannerException(Exception):
    """Base exception."""


class ConfigurationError(ScannerException):
    """Invalid configuration."""


class ConnectionError(ScannerException):
    """HTTP/Network failure."""


class DhanConnectionError(ConnectionError):
    """Dhan connection failure."""


class DataValidationError(ScannerException):
    """Invalid market data."""


class WatchlistError(ScannerException):
    """Watchlist related error."""