from typing import Union, Set

from allocation.protocols.sat import SAT
from allocation.protocols.types import Interpretation

from allocation.entities.formula import Formula, Atom, Not, And
from allocation.utils.propositional_logic.functions import atoms
from allocation.utils.propositional_logic.semantics import truth_value


class BruteForceSAT(SAT):
    def __init__(self, formula: Formula):
        self._formula = formula
        self._get_atoms = atoms
        self._truth_value = truth_value

    def is_satisfiable(self) -> Union[Interpretation, bool]:
        set_atoms = self._get_atoms(self._formula)
        interpretation = self._get_partial_interpretation(self._formula)
        if interpretation:
            set_atoms = self._new_set_atoms(set_atoms, interpretation)
            return self._check(set_atoms, interpretation)
        return self._check(set_atoms, set())

    def _check(self, set_atoms: Set[Atom], interpretation: Interpretation) -> Union[Interpretation, bool]:
        if len(set_atoms) == 0:
            if self._truth_value(self._formula, interpretation):
                return interpretation
            return False
        # Gera cópias
        set_atoms_copy = set_atoms.copy()
        atom = set_atoms_copy.pop()
        interpretation_copy = interpretation.copy()

        interpretation1 = interpretation_copy.union({(atom, True)})
        interpretation2 = interpretation_copy.union({(atom, False)})

        result = self._check(set_atoms_copy, interpretation1)
        if result:
            return result
        return self._check(set_atoms_copy, interpretation2)

    @classmethod
    def _get_partial_interpretation(cls, formula: Formula) -> Union[Interpretation, None]:
        """
        Returns a partial interpretation if possible. Otherwise, it returns None.
        """

        if isinstance(formula, Atom):
            return {(formula, True)}
        if isinstance(formula, Not):
            if isinstance(formula.inner, Atom):
                return {(formula.inner, False)}
        if isinstance(formula, And):
            left = cls._get_partial_interpretation(formula.left)
            right = cls._get_partial_interpretation(formula.right)
            if left:
                if right:
                    return left.union(right)
                return left
            if right:
                return right
            return None

    @staticmethod
    def _new_set_atoms(set_atoms: Set[Atom], interpretation: Interpretation):
        return set(filter(
            lambda atom:
            not (interpretation.issuperset({(atom, True)}) or interpretation.issuperset({(atom, False)})),
            set_atoms
        ))
