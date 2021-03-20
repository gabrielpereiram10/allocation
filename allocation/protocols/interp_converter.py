from typing import Protocol, Set
from abc import abstractmethod

from allocation.protocols.types import Interpretation


class InterpConverter(Protocol):
    @abstractmethod
    def to_interp(self, int_interp: Set[int]) -> Interpretation:
        raise NotImplemented
