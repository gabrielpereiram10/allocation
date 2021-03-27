from statistics import multimode
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
        literal = self._choose_literal(clauses)
        left = {frozenset({literal})}.union(clauses.copy())
        result = self._sat(left, interpretation.copy())
        if result:
            return result
        right = {frozenset({literal * -1})}.union(clauses.copy())
        return self._sat(right, interpretation.copy())

    def _choose_literal(self, clauses: Set[FrozenSet[int]]) -> int:
        literals = self._get_multi_mode(clauses)
        ordered_clauses = sorted(clauses, key=len)
        for clause in ordered_clauses:
            intersection_of_literals = set(literals).intersection(clause)
            if intersection_of_literals:
                return intersection_of_literals.pop()

    @staticmethod
    def _get_multi_mode(clauses: Set[FrozenSet[int]]):
        literals = []
        for clause in clauses:
            literals.extend(list(clause))
        return multimode(literals)

    def _unit_propagation(self, clauses: Set[FrozenSet[int]], interpretation: Set[int]) -> Tuple[
        ClausesOfIntegers, Set[int]]:
        while True:
            literal = self._literal_unit(clauses)
            if not literal:
                break
            interpretation = interpretation.union({literal})
            clauses = self._remove_clauses_with_literal(clauses, literal)
            clauses = self._remove_complement_literal(clauses, literal)
        return clauses, interpretation

    @staticmethod
    def _remove_clauses_with_literal(clauses: Set[FrozenSet[int]], literal: int) -> Set[FrozenSet[int]]:
        return set(filter(lambda c: literal not in c, clauses))

    @staticmethod
    def _remove_complement_literal(clauses: Set[FrozenSet[int]], literal: int) -> Set[FrozenSet[int]]:
        return set(map(lambda c: c.difference({literal * -1}), clauses))

    @staticmethod
    def _literal_unit(clauses: Set[FrozenSet[int]]) -> int:
        for clause in clauses:
            if len(clause) == 1:
                return list(clause)[0]
