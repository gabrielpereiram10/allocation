from typing import Set, Tuple, FrozenSet, List

from allocation.entities.formula import Atom, Formula
from allocation.entities.discipline import Discipline

Interpretation = Set[Tuple[Atom, bool]]
ClausesOfFormulas = Set[FrozenSet[Formula]]
ClausesOfIntegers = Set[FrozenSet[int]]
Disciplines = List[Discipline]
Schedules = List[List]
