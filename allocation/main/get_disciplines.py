import csv
import os
import pathlib

from allocation.entities.discipline import Discipline


def get_disciplines():
    file = os.path.abspath('../../tests/disciplines01.txt')
    with open(file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return [Discipline(**line) for line in reader]
