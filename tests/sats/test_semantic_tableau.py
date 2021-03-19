import unittest

from allocation.sats.semantic_tableau import SemanticTableauSAT
from allocation.entities.formula import Atom, Not, And, Or, Implies


class SemanticTableauTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.sat = SemanticTableauSAT

    def test_for_premises_that_contain_complementary_formulas(self):
        p, q = Atom('p'), Atom('q')
        premises = [
            {p, Not(p)}, {And(p, q), Not(And(p, q))}
        ]
        for i in range(len(premises)):
            with self.subTest(i=i):
                self.assertFalse(self.sat(premises[i]).is_satisfiable())

    def test_for_alpha_formulas(self):
        p, q = Atom('p'), Atom('q')
        premises = [
            {Not(Not(p))}, {Not(Or(p, q))}, {Not(Implies(p, q))}, {And(p, q)}
        ]
        results = [
            {(p, True)}, {(p, False), (q, False)}, {(p, True), (q, False)}, {(p, True), (q, True)}
        ]
        for i in range(len(premises)):
            with self.subTest(i=i):
                self.assertSetEqual(results[i], self.sat(premises[i]).is_satisfiable())

    def test_for_beta_formulas(self):
        p, q = Atom('p'), Atom('q')
        premises = [
            {Not(And(p, q))}, {Implies(p, q)}, {Or(p, q)}
        ]
        results = [
            {(p, False), (q, True)}, {(p, False), (q, True)}, {(p, True), (q, True)}
        ]
        for i in range(len(premises)):
            with self.subTest(i=i):
                self.assertSetEqual(results[i], self.sat(premises[i]).is_satisfiable())


if __name__ == '__main__':
    unittest.main()
