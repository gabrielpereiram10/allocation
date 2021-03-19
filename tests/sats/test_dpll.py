import os

from allocation.utils.cnf.cnf_file import CNFFile
from allocation.sats.dpll import DPLL

satisfiable_path = os.path.abspath('../../cnf-formulas/satisfiable')
satisfiable_formulas = os.listdir(satisfiable_path)
[print(DPLL(CNFFile.from_file(f'{satisfiable_path}/{i}')).is_satisfiable_test()) for i in satisfiable_formulas]

unsatisfiable_path = os.path.abspath('../../cnf-formulas/unsatisfiable')
unsatisfiable_formulas = os.listdir(unsatisfiable_path)
[print(DPLL(CNFFile.from_file(f'{unsatisfiable_path}/{i}')).is_satisfiable_test()) for i in unsatisfiable_formulas]
