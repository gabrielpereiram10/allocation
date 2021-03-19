from typing import NoReturn

from allocation.utils.big_formula import BigFormula
from allocation.protocols.types import Disciplines


class AllocatorConstraintBase:
    _big_formula = BigFormula

    def __init__(self, disciplines: Disciplines, schedules_quantity: int):
        self.disciplines = disciplines
        self.schedules_quantity = schedules_quantity

    @property
    def disciplines(self) -> Disciplines:
        return self._disciplines

    @disciplines.setter
    def disciplines(self, disciplines: Disciplines):
        if not disciplines:
            raise ValueError('Disciplines quantity cannot be less than one.')
        self._disciplines = disciplines

    @property
    def schedules_quantity(self) -> int:
        return self._schedules_quantity

    @schedules_quantity.setter
    def schedules_quantity(self, value: int) -> NoReturn:
        if value < 1:
            raise ValueError('Schedules quantity cannot be less than one.')
        self._schedules_quantity = value
