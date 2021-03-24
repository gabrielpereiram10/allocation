from typing import Union

from pysat.solvers import Glucose4

from allocation.protocols.sat import SAT
from allocation.protocols.types import Interpretation, ClausesOfIntegers
from allocation.protocols.interp_converter import InterpConverter


class PySATAdapter(SAT):
    def __init__(self, clauses: ClausesOfIntegers, converter: InterpConverter = None):
        self._clauses = clauses
        self._converter = converter
        self._solver = Glucose4()

    def is_satisfiable(self) -> Union[Interpretation, bool]:
        [self._solver.add_clause(list(clause)) for clause in self._clauses]
        if self._solver.solve():
            return self._converter.to_interp(set(self._solver.get_model()))
        return False

    def is_satisfiable_test(self):
        [self._solver.add_clause(clause) for clause in self._clauses]
        if self._solver.solve():
            return self._solver.get_model()
        return False
