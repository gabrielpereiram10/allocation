from typing import List, NoReturn

from allocation.protocols.types import ClausesOfIntegers


class CNFFile:
    @staticmethod
    def from_file(file_name: str) -> ClausesOfIntegers:
        clauses = set()
        with open(file_name, 'r') as cnf_file:
            lines = cnf_file.readlines()
            for line in lines:
                line = line.strip()
                if line and line[0] not in ['p', 'c', '%', '0']:
                    clause = frozenset([int(literal) for literal in line.split()[:-1]])
                    clauses.add(clause)
        return clauses

    @staticmethod
    def to_file(file_name: str, clauses: ClausesOfIntegers, comments: List[str]) -> NoReturn:
        with open(f'{file_name}.cnf', 'x') as cnf:
            lines = []
            for comment in comments:
                lines.append('c ' + ''.join(comment) + '\n')
            lines.append(f'p cnf {len(clauses)}\n')
            for clause in clauses:
                lines.append(' '.join(str(literal) for literal in clause) + ' 0\n')
            cnf.writelines(lines)
