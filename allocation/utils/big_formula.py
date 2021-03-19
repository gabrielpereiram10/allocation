from typing import List, Union
from functools import reduce

from allocation.entities.formula import And, Formula, Or


class BigFormula:
    @staticmethod
    def and_all(formulas: List[Formula]) -> Union[Formula, bool]:
        if not formulas:
            return False
        if len(formulas) == 1:
            return formulas[0]
        return reduce(lambda x, y: And(x, y), formulas)

    @staticmethod
    def or_all(formulas: List[Formula]) -> Union[Formula, bool]:
        if not formulas:
            return False
        if len(formulas) == 1:
            return formulas[0]
        return reduce(lambda x, y: Or(x, y), formulas)
