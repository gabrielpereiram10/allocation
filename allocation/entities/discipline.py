class Discipline:
    def __init__(self, semester, nome, professor):
        self.semester = semester
        self.nome = nome
        self.professor = professor

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Discipline) and other.nome == self.nome and other.semester == self.semester and other.professor == self.professor

    def __repr__(self) -> str:
        return f'{self.nome}'

    def __str__(self) -> str:
        return self.__repr__()
