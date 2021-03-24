import pandas as pd
from statistics import fmean
from typing import List

from allocation.protocols.types import Disciplines
from allocation.main.main import to_model, atoms_map
from allocation.utils.literal_converter import LiteralConverter
from allocation.utils.cnf.clausal_form_converter import ClausalFormConverter
from allocation.main.allocator import Allocator

from allocation.sats.brute_force import BruteForceSAT
from allocation.sats.semantic_tableau import SemanticTableauSAT
from allocation.sats.dpll import DPLL
from allocation.sats.pysat_adapter import PySATAdapter

from allocation.main.get_disciplines import get_disciplines


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
