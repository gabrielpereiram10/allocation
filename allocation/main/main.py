from allocation.main.get_disciplines import get_disciplines
from allocation.entities.formula import Atom
from allocation.constraints import constraints
from allocation.constraints.composite import ConstraintComposite

from allocation.sats.brute_force import BruteForceSAT
from allocation.sats.semantic_tableau import SemanticTableauSAT
from allocation.sats.dpll import DPLL
from allocation.sats.pysat_adapter import PySATAdapter

from allocation.utils.cnf.clausal_form_converter import ClausalFormConverter
from allocation.utils.literal_converter import LiteralConverter
from allocation.main.execute import Allocator


disciplines = get_disciplines()
schedules = [
    [], [], [], [], [],
    [], [], [], [], []
]


def atoms_map(n_disciplines: int, n_schedules: int):
    dict_map = {}
    count = 0
    for i in range(n_disciplines):
        for j in range(n_schedules):
            count += 1
            dict_map[Atom(f'{i + 1}_{j + 1}')] = count
    return dict_map


def to_model(disciplines, n_schedules):
    composite01 = ConstraintComposite()
    composite01.add_all([constraint(disciplines, n_schedules) for constraint in constraints])
    return composite01.apply()


model = to_model(disciplines, 3)
brute_force = BruteForceSAT(model)
tableau = SemanticTableauSAT({model})

dict_map = atoms_map(len(disciplines), 3)
converter = LiteralConverter(dict_map)
cnf_model = converter.to_clauses_of_int(ClausalFormConverter.convert(model))
dpll = DPLL(cnf_model, converter)
py_sat = PySATAdapter(cnf_model, converter)


Allocator(disciplines, 3).execute([brute_force, tableau, dpll, py_sat])
