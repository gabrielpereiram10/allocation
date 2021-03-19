from typing import Protocol, Union
from abc import abstractmethod

from allocation.entities.formula import Formula


class IConstraint(Protocol):
    @abstractmethod
    def apply(self) -> Union[Formula, bool]:
        raise NotImplemented
