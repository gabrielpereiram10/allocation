from typing import Set, Union, Tuple

from allocation.protocols.sat import SAT
from allocation.entities.formula import Formula, Atom, Not, And, Or, Implies
from allocation.utils.propositional_logic.functions import atoms
from allocation.protocols.types import Interpretation


class SemanticTableauSAT(SAT):
    def __init__(self, premises: Set[Formula]):
        self._premises = premises
        self._atoms = atoms

    def is_satisfiable(self) -> Union[Interpretation, bool]:
        result = self._check(self._premises.copy())
        if result:
            return self._find_interpretation(result, self._get_atoms())
        return False

    def _check(self, premises: Set[Formula]) -> Set[Formula]:
        if self._contains_complementary(premises):
            return set()
        premise = self._get_alpha_formula(premises)
        if premise:
            premises.remove(premise)
            return self._check(premises.union(self._apply_alpha_rule(premise)))
        premise = self._get_beta_formula(premises)
        if premise:
            premises.remove(premise)
            left, right = self._apply_beta_rule(premise)
            result = self._check(premises.union({left}))
            if result:
                return result
            return self._check(premises.union({right}))
        return premises

    @staticmethod
    def _contains_complementary(premises: Set[Formula]) -> bool:
        for premise in premises:
            if Not(premise) in premises:
                return True
        return False

    @staticmethod
    def _get_alpha_formula(premises: Set[Formula]) -> Union[Formula, None]:
        for premise in premises:
            if isinstance(premise, Not) and type(premise.inner) in [Not, Or, Implies]:
                return premise
            if isinstance(premise, And):
                return premise
        return None

    @staticmethod
    def _apply_alpha_rule(premise: Formula) -> Set[Formula]:
        if isinstance(premise, Not):
            if isinstance(premise.inner, Not):
                return {premise.inner.inner}
            if isinstance(premise.inner, Or):
                return {Not(premise.inner.left), Not(premise.inner.right)}
            if isinstance(premise.inner, Implies):
                return {premise.inner.left, Not(premise.inner.right)}
        return {premise.left, premise.right}

    def _get_atoms(self) -> Set[Atom]:
        set_atoms = set()
        for premise in self._premises:
            set_atoms = set_atoms.union(self._atoms(premise))
        return set_atoms

    @staticmethod
    def _find_interpretation(literals: Set[Formula], all_atoms: Set[Atom]) -> Interpretation:
        interpretation = set()
        for atom in all_atoms:
            if Not(atom) in literals:
                interpretation.add((atom, False))
            else:
                interpretation.add((atom, True))
        return interpretation

    @staticmethod
    def _get_beta_formula(premises: Set[Formula]) -> Union[Formula, None]:
        for premise in premises:
            if isinstance(premise, Not) and isinstance(premise.inner, And):
                return premise
            if type(premise) in [Or, Implies]:
                return premise
        return None

    @staticmethod
    def _apply_beta_rule(premise: Formula) -> Tuple[Formula, Formula]:
        if isinstance(premise, Not) and isinstance(premise.inner, And):
            return Not(premise.inner.left), Not(premise.inner.right)
        if isinstance(premise, Implies):
            return Not(premise.left), premise.right
        return premise.left, premise.right
