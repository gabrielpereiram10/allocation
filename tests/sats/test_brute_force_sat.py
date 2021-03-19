import unittest

from allocation.sats.brute_force import BruteForceSAT
from allocation.entities.formula import Atom, Not, Or, And, Implies


class BruteForceSATTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.sat = BruteForceSAT
        self.p, self.q, self.r = Atom('p'), Atom('q'), Atom('r')

    def test_for_unsatisfiable_formulas(self):
        formulas = [
            Not(Implies(self.p, Or(self.p, self.q))), And(self.p, Not(self.p)),
            Not(Implies(self.p, Or(self.p, self.q)))
        ]
        for i in range(len(formulas)):
            with self.subTest(i=i):
                self.assertFalse(self.sat(formulas[i]).is_satisfiable())

    def test_for_satisfiable_formulas(self):
        formulas = [
            Not(Implies(Or(self.p, self.q), self.p)),
            Not(And(Implies(self.q, Not(self.p)), Implies(self.p, Or(self.r, self.q)))),
        ]
        results = [
            [{(self.p, False), (self.q, True)}],
            [{(self.p, True), (self.q, True), (self.r, True)},
             {(self.p, True), (self.q, True), (self.r, False)},
             {(self.p, True), (self.q, False), (self.r, False)}],
        ]
        for i in range(len(formulas)):
            with self.subTest(i=i):
                self.assertIn(self.sat(formulas[i]).is_satisfiable(), results[i])


if __name__ == '__main__':
    unittest.main()
