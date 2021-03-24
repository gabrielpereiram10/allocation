import time
from typing import List

from allocation.protocols.types import Disciplines
from allocation.protocols.sat import SAT


class Allocator:
    def __init__(self, disciplines: Disciplines, n_schedules: int):
        self._disciplines = disciplines
        self._n_schedules = n_schedules

    def execute(self, sats: List[SAT]):
        for sat in sats:
            start = time.time()
            result = sat.is_satisfiable()
            end = time.time()
            print(f'Time: {end - start}')
            if result:
                self.show(self.interpretation_adapt(result))
            else:
                print(False)

    @classmethod
    def time_test(cls, sat: SAT):
        start = time.time()
        result = sat.is_satisfiable()
        end = time.time()
        test_time = end - start
        return test_time

    def interpretation_adapt(self, interp):
        disciplines_copy = self._disciplines.copy()
        schedules = [[] for i in range(self._n_schedules)]
        interp = set(filter(lambda t: t[1] is True, interp))
        for i in interp:
            name = i[0].name.split('_')
            schedules[int(name[1]) - 1].append(disciplines_copy[int(name[0]) - 1])
        return schedules

    @staticmethod
    def show(schedules):
        for i, schedule in enumerate(schedules):
            print(f'{i + 1}: ', end='')
            for j, discipline in enumerate(schedule):
                if j == len(schedule) - 1:
                    print(f'{discipline}', end='.')
                else:
                    print(f'{discipline}', end=', ')
            print()
