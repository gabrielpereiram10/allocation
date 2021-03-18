from allocation.entities.formula import *
from allocation.protocols.types import Interpretation


def truth_value(formula: Formula, interpretation: Interpretation) -> Union[bool, None]:
    """
    Determines the true value of a formula for an interpretation (evaluation) complete or partial.
    An interpretation can be defined as a set of tuples. For example, {(Atom('p'), True)}.
    """

    if isinstance(formula, Atom):
        return formula.get_value(interpretation)
    if isinstance(formula, Not):
        return Not(
            truth_value(formula.inner, interpretation)
        ).truth_value()
    if isinstance(formula, BinaryConnective):
        return type(formula)(
            truth_value(formula.left, interpretation),
            truth_value(formula.right, interpretation)
        ).truth_value()
