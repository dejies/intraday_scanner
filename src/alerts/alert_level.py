from enum import Enum


class AlertLevel(str, Enum):

    LOW = "LOW"

    MEDIUM = "MEDIUM"

    HIGH = "HIGH"

    VERY_HIGH = "VERY_HIGH"