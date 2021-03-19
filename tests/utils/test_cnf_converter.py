import unittest
from typing import List

from allocation.utils.cnf.cnf_converter import CNFConverter
from allocation.entities.formula import Atom, And, Or, Not, Implies, Formula


class CNFConverterTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.cnf_converter = CNFConverter
        self.p, self.q, self.r, self.s = Atom('p'), Atom('q'), Atom('r'), Atom('s')

    def test_implication_free(self):
        formulas = [
            self.r, Implies(self.p, self.q),
            And(Implies(self.p, self.q), Implies(self.p, self.r)), Not(Implies(self.p, self.r))
        ]
        result = [
            self.r, Or(Not(self.p), self.q),
            And(Or(Not(self.p), self.q), Or(Not(self.p), self.r)), Not(Or(Not(self.p), self.r))
        ]
        for i in range(len(formulas)):
            with self.subTest(i=i):
                self.assertEqual(result[i], self.cnf_converter._implication_free(formulas[i]))

    def test_negation_normal_form(self):
        formulas = [
            self.p, Not(self.p), Not(Not(self.p)), And(Not(self.p), Not(Not(self.q))),
            Not(And(self.p, self.q)), Not(Or(self.q, Not(self.r)))
        ]
        result = [
            self.p, Not(self.p), self.p, And(Not(self.p), self.q),
            Or(Not(self.p), Not(self.q)), And(Not(self.q), self.r)
        ]
        self.execute_sub_tests(formulas, result)

    def test_distributive(self):
        formulas = [
            self.p, Not(self.p), And(Not(self.p), self.q),
            Or(And(self.p, self.q), Not(self.r)),
            Or(self.p, And(Not(self.q), Not(self.r)))
        ]
        result = [
            self.p, Not(self.p), And(Not(self.p), self.q),
            And(Or(self.p, Not(self.r)), Or(self.q, Not(self.r))),
            And(Or(self.p, Not(self.q)), Or(self.p, Not(self.r)))
        ]
        self.execute_sub_tests(formulas, result)

    def execute_sub_tests(self, formulas: List[Formula], result: List[Formula]) -> None:
        for i in range(len(formulas)):
            with self.subTest(i=i):
                self.assertEqual(result[i], self.cnf_converter.convert(formulas[i]))


if __name__ == '__main__':
    unittest.main()
