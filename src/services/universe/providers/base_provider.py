from abc import ABC
from abc import abstractmethod

from src.services.universe.models import UniverseStock


class MarketUniverseProvider(ABC):

    @abstractmethod
    def load(self) -> list[UniverseStock]:
        """
        Returns all constituents
        from this provider.
        """
        raise NotImplementedError