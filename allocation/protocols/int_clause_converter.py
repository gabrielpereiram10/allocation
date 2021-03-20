from typing import Protocol, Set
from abc import abstractmethod

from allocation.protocols.types import ClausesOfFormulas, ClausesOfIntegers


class IntClausesConverter(Protocol):
    @abstractmethod
    def to_clauses_of_int(self, clauses: ClausesOfFormulas) -> ClausesOfIntegers:
        raise NotImplemented
