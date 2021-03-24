import csv
import os

from allocation.entities.discipline import Discipline


def get_disciplines():
    path = os.path.abspath('../../inputs')
    filenames = sorted(os.listdir(path), key=len)
    disciplines = []
    for filename in filenames:
        with open(f'{path}/{filename}', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            disciplines.append([Discipline(**line) for line in reader])
    return disciplines
