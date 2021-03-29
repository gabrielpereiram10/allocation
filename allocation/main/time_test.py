import pandas as pd
from statistics import fmean
from typing import List

from allocation.protocols.types import Disciplines
from allocation.utils.literal_converter import LiteralConverter
from allocation.utils.cnf.clausal_form_converter import ClausalFormConverter
from allocation.main.allocator import Allocator

from allocation.sats.brute_force import BruteForceSAT
from allocation.sats.semantic_tableau import SemanticTableauSAT
from allocation.sats.dpll import DPLL
from allocation.sats.pysat_adapter import PySATAdapter

from allocation.main import get_disciplines, atoms_map, to_model


def to_test(disciplines_list: List[Disciplines]):
    schedules = [10, 3, 3, 3, 3, 2, 2, 3, 3, 2, 3]
    models = []
    atoms_maps = []
    converters = []
    cnf_models = []
    for i, disciplines in enumerate(disciplines_list):
        model = to_model(disciplines, schedules[i])
        dict_map = atoms_map(len(disciplines), schedules[i])
        converter = LiteralConverter(dict_map)

        models.append(model)
        atoms_maps.append(dict_map)
        converters.append(converter)
        cnf_models.append(converter.to_clauses_of_int(ClausalFormConverter.convert(model)))
    brute_force_test = [Allocator.time_test(BruteForceSAT(model)) for i, model in enumerate(models[1:])]
    tableau_test = [Allocator.time_test(SemanticTableauSAT({model})) for i, model in enumerate(models[1:])]
    dpll_test = [Allocator.time_test(DPLL(cnf_models[i], converters[i])) for i, model in enumerate(models)]
    py_sat_test = [Allocator.time_test(PySATAdapter(cnf_models[i], converters[i])) for i, model in enumerate(models)]
    brute_force_test.insert(0, None)
    tableau_test.insert(0, None)
    tests = [brute_force_test, tableau_test, dpll_test, py_sat_test]
    df = pd.DataFrame({'Variables Quantity': [len(dict_map) for dict_map in atoms_maps] + ['mean'],
                       'Brute Force': tests[0] + [fmean(brute_force_test[1:])],
                       'Semantic Tableau': tests[1] + [fmean(tableau_test[1:])],
                       'DPLL': tests[2] + [fmean(dpll_test)],
                       'PySAT': tests[3] + [fmean(py_sat_test)]})
    print(df)


to_test(get_disciplines())

"""
   Variables Quantity  Brute Force  Semantic Tableau      DPLL     PySAT
0                 230          NaN               NaN  0.593715  0.015598
1                   9     0.015618          0.000000  0.000000  0.000000
2                  12     0.124990          0.000000  0.000000  0.000000
3                  12     0.140615          0.000000  0.000000  0.000000
4                  15     0.812443          0.046872  0.000000  0.000000
5                  10     0.015624          0.000000  0.000000  0.000000
6                  10     0.015624          0.000000  0.000000  0.000000
7                  18     7.327612          0.093743  0.000000  0.000000
8                  18     9.934578          0.234359  0.000000  0.000000
9                  14     2.562340          0.156240  0.000000  0.000000
10                 21    61.299859          2.843550  0.000000  0.000000
11               mean     8.224930          0.337476  0.053974  0.001418

------------------------------------------------------------------------

   Variables Quantity  Brute Force  Semantic Tableau      DPLL    PySAT
0                 230          NaN               NaN  0.593717  0.01562
1                   9     0.031247          0.000000  0.000000  0.00000
2                  12     0.031248          0.015625  0.000000  0.00000
3                  12     0.031268          0.000000  0.000000  0.00000
4                  15     0.312458          0.015625  0.000000  0.00000
5                  10     0.031268          0.000000  0.000000  0.00000
6                  10     0.000000          0.000000  0.000000  0.00000
7                  18     6.921390          0.015645  0.000000  0.00000
8                  18    10.209905          0.015601  0.000000  0.00000
9                  14     2.702935          0.203133  0.000000  0.00000
10                 21    49.006691         11.921019  0.000000  0.00000
11               mean     6.927841          1.218665  0.053974  0.00142
"""
