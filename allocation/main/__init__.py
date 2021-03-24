import os
import csv

from allocation.entities.discipline import Discipline
from allocation.entities.formula import Atom

from allocation.constraints import constraints
from allocation.constraints.composite import ConstraintComposite


def get_disciplines():
    path = os.path.abspath('../../inputs')
    filenames = sorted(os.listdir(path), key=len)
    disciplines = []
    for filename in filenames:
        with open(f'{path}/{filename}', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            disciplines.append([Discipline(**line) for line in reader])
    return disciplines


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
