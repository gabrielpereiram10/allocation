from typing import Protocol, Union
from abc import abstractmethod

from allocation.protocols.types import Interpretation


class SAT(Protocol):
    @abstractmethod
    def is_satisfiable(self) -> Union[Interpretation, bool]:
        raise NotImplemented
