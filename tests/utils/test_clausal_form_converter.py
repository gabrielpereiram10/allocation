import unittest

from allocation.utils.cnf.clausal_form_converter import ClausalFormConverter
from allocation.entities.formula import Atom, Not, And, Implies, Or


class ClauseNFConverterTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.converter = ClausalFormConverter

    def test_convert(self):
        c = Atom('c')
        i = Atom('i')
        p = Atom('p')
        q = Atom('q')
        s = Atom('s')
        r = Atom('r')
        n = Atom('n')
        formulas = [
            And(And(Implies(And(c, i), Not(s)), Not(c)), Not(Implies(s, Not(i)))),
            And(And(Implies(c, Or(i, r)), Implies(Or(i, r), n)), Not(Implies(c, n))),
            Implies(Or(p, q), Not(Or(q, r)))
        ]
        result = [
            {frozenset([Not(c), Not(i), Not(s)]), frozenset([Not(c)]), frozenset([s]), frozenset([i])},
            {frozenset([Not(c), i, r]), frozenset([Not(i), n]), frozenset([Not(r), n]), frozenset([c]), frozenset([Not(n)])},
            {frozenset([Not(p), Not(q)]), frozenset([Not(q)]), frozenset([Not(p), Not(r)]), frozenset([Not(q), Not(r)])}
        ]
        for i in range(len(formulas)):
            with self.subTest(i=i):
                self.assertSetEqual(result[i], self.converter.convert(formulas[i]))


if __name__ == '__main__':
    unittest.main()
