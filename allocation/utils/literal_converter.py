from typing import Set, Dict

from allocation.protocols.interp_converter import InterpConverter
from allocation.protocols.int_clause_converter import IntClausesConverter
from allocation.protocols.types import ClausesOfFormulas, Interpretation, ClausesOfIntegers

from allocation.entities.formula import Not, Atom


class LiteralConverter(InterpConverter, IntClausesConverter):
    def __init__(self, literals_map: Dict[Atom, int]):
        self._literals_map = literals_map

    def to_interp(self, int_interp: Set[int]) -> Interpretation:
        converted_inter = set()
        for i in int_interp:
            for k, v in self._literals_map.items():
                if v == i:
                    converted_inter.add((k, True))
                elif v * -1 == i:
                    converted_inter.add((Not(k), False))
        return converted_inter

    def to_clauses_of_int(self, clauses: ClausesOfFormulas) -> ClausesOfIntegers:
        converted_clauses = set()
        for clause in clauses:
            converted_clause = []
            for literal in clause:
                if isinstance(literal, Not):
                    converted_clause.append(self._literals_map[literal.inner] * -1)
                else:
                    converted_clause.append(self._literals_map[literal])
            converted_clauses.add(frozenset(converted_clause))
        return converted_clauses
