"""This module is designed to define formulas in propositional logic.
For example, the following piece of code creates an object representing (p v s).

formula1 = Or(Atom('p'), Atom('s'))


As another example, the piece of code below creates an object that represents (p → (p v s)).

formula2 = Implies(Atom('p'), Or(Atom('p'), Atom('s')))
"""

from abc import abstractmethod
from typing import Union, Set, Sized


class Formula:
    ...


class Connective(Formula):
    @abstractmethod
    def truth_value(self) -> Union[bool, None]:
        """
        Returns the true value of the operation.
        If not, return None.
        """
        raise NotImplemented


class BinaryConnective(Connective):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Atom(Formula):
    """
    This class represents propositional logic variables.
    """

    def __init__(self, name):
        super().__init__()
        self.name = name

    def get_value(self, interpretation: Set) -> Union[bool, None]:
        """
        Checks if Atom is in the interpretation and returns the associated value.
        Otherwise, it returns None.
        :param interpretation: A set of tuples containing an atom and its associated value
        """

        if interpretation.issuperset({(self, True)}):
            return True
        if interpretation.issuperset({(self, False)}):
            return False
        return None

    @staticmethod
    def __is_empty(iterable: Sized) -> bool:
        return len(iterable) == 0

    def __repr__(self):
        return str(self.name)

    def __eq__(self, other):
        return isinstance(other, Atom) and other.name == self.name

    def __hash__(self):
        return hash((self.name, 'atom'))


class Implies(BinaryConnective):

    def __init__(self, left, right):
        super().__init__(left, right)

    def truth_value(self) -> Union[bool, None]:
        if self.left is False or self.right is True:
            return True
        if self.left is True and self.right is False:
            return False
        return None

    def __repr__(self):
        return "(" + self.left.__str__() + " " + u"\u2192" + " " + self.right.__str__() + ")"

    def __eq__(self, other):
        return isinstance(other, Implies) and other.left == self.left and other.right == self.right

    def __hash__(self):
        return hash((hash(self.left), hash(self.right), 'implies'))


class Not(Connective):

    def __init__(self, inner):
        super().__init__()
        self.inner = inner

    def truth_value(self) -> Union[bool, None]:
        if isinstance(self.inner, bool):
            return not self.inner
        return None

    def __repr__(self):
        return "(" + u"\u00ac" + str(self.inner) + ")"

    def __eq__(self, other):
        return isinstance(other, Not) and other.inner == self.inner

    def __hash__(self):
        return hash((hash(self.inner), 'not'))


class And(BinaryConnective):

    def __init__(self, left, right):
        super().__init__(left, right)

    def truth_value(self) -> Union[bool, None]:
        if self.left is True and self.right is True:
            return True
        if self.left is False or self.right is False:
            return False
        return None

    def __repr__(self):
        return "(" + self.left.__str__() + " " + u"\u2227" + " " + self.right.__str__() + ")"

    def __eq__(self, other):
        return isinstance(other, And) and other.left == self.left and other.right == self.right

    def __hash__(self):
        return hash((hash(self.left), hash(self.right), 'and'))


class Or(BinaryConnective):

    def __init__(self, left, right):
        super().__init__(left, right)

    def truth_value(self) -> Union[bool, None]:
        if self.left is True or self.right is True:
            return True
        if self.left is False and self.right is False:
            return False
        return None

    def __repr__(self):
        return "(" + self.left.__str__() + " " + u"\u2228" + " " + self.right.__str__() + ")"

    def __eq__(self, other):
        return isinstance(other, Or) and other.left == self.left and other.right == self.right

    def __hash__(self):
        return hash((hash(self.left), hash(self.right), 'or'))


class Iff(BinaryConnective):

    def __init__(self, left, right):
        super().__init__(left, right)

    def truth_value(self) -> Union[bool, None]:
        if isinstance(self.left, bool) and isinstance(self.right, bool):
            if self.left == self.right:
                return True
            return False
        return None

    def __repr__(self):
        return "(" + self.left.__str__() + " " + u"\u2194" + " " + self.right.__str__() + ")"

    def __eq__(self, other):
        return isinstance(other, Iff) and other.left == self.left and other.right == self.right

    def __hash__(self):
        return hash((hash(self.left), hash(self.right), 'iff'))


class Xor(BinaryConnective):

    def __init__(self, left, right):
        super().__init__(left, right)

    def truth_value(self) -> Union[bool, None]:
        if isinstance(self.left, bool) and isinstance(self.right, bool):
            if self.left != self.right:
                return True
            return False
        return None

    def __repr__(self):
        return "(" + self.left.__str__() + " " + u"\u2295" + " " + self.right.__str__() + ")"

    def __eq__(self, other):
        return isinstance(other, Xor) and other.left == self.left and other.right == self.right

    def __hash__(self):
        return hash((hash(self.left), hash(self.right), 'xor'))
