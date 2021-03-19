from typing import Set, Tuple, FrozenSet

from allocation.entities.formula import Atom, Formula

Interpretation = Set[Tuple[Atom, bool]]
ClausesOfFormulas = Set[FrozenSet[Formula]]
ClausesOfIntegers = Set[FrozenSet[int]]
