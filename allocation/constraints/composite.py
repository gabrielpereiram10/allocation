from typing import List, NoReturn, Union

from allocation.protocols.constraint import IConstraint
from allocation.entities.formula import Formula
from allocation.utils.big_formula import BigFormula


class ConstraintComposite(IConstraint):
    _big_formula = BigFormula

    def __init__(self):
        self._constraints: List[IConstraint] = []

    def add(self, constraint: IConstraint) -> NoReturn:
        self._constraints.append(constraint)

    def add_all(self, constraints: List[IConstraint]) -> NoReturn:
        self._constraints.extend(constraints)

    def apply(self) -> Union[Formula, bool]:
        formulas = []
        for constraint in self._constraints:
            formulas.append(constraint.apply())
        formulas = list(filter(lambda formula: formula is not False, formulas))
        if not formulas:
            return False
        return self._big_formula.and_all(formulas)
