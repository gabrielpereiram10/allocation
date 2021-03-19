from typing import Union, Set, FrozenSet, Tuple

from allocation.protocols.sat import SAT
from allocation.protocols.types import ClausesOfIntegers, Interpretation
from allocation.protocols.interp_converter import InterpConverter


class DPLL(SAT):
    def __init__(self, clauses: ClausesOfIntegers, converter: InterpConverter = None):
        self._clauses = clauses
        self._converter = converter

    def is_satisfiable(self) -> Union[Interpretation, bool]:
        result = self._sat(self._clauses, set())
        if result:
            return self._converter.to_interp(result)
        return False

    def is_satisfiable_test(self) -> Union[Set[int], bool]:
        return self._sat(self._clauses, set())

    def _sat(self, clauses: ClausesOfIntegers, interpretation: Set[int]) -> Union[Set[int], bool]:
        clauses, interpretation = self._unit_propagation(clauses, interpretation.copy())
        if len(clauses) == 0:
            return interpretation
        if set() in clauses:
            return False
        literal = self._get_literal(clauses)
        left = {frozenset({literal})}.union(clauses.copy())
        result = self._sat(left, interpretation.copy())
        if result:
            return result
        right = {frozenset({literal * -1})}.union(clauses.copy())
        return self._sat(right, interpretation.copy())

    @staticmethod
    def _get_literal(clauses: Set[FrozenSet[int]]) -> int:
        c = None
        for clause in clauses.copy():
            if not c or len(clause) < len(c):
                c = set(clause)
        return c.pop()

    def _unit_propagation(self, clauses: Set[FrozenSet[int]], interpretation: Set[int]) -> Tuple[ClausesOfIntegers, Set[int]]:
        unit_clauses_literals = set(map(lambda x: set(x).pop(), filter(self._is_unit_clause, clauses)))
        if not unit_clauses_literals:
            return clauses, interpretation
        new_clauses = set()
        interpretation = interpretation.union(unit_clauses_literals)
        for literal in unit_clauses_literals:
            clauses = set(filter(lambda c: literal not in c, clauses))
            for clause in clauses:
                new_clauses.add(clause.difference({literal * -1}))
        return new_clauses, interpretation

    @staticmethod
    def _is_unit_clause(clause: FrozenSet[int]) -> bool:
        return len(clause) == 1
