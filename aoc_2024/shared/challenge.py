from abc import abstractmethod, ABCMeta
from dataclasses import dataclass
from timeit import timeit


@dataclass
class DaySolutionDTO:
    solution_part1: str
    solution_part2: str


class Challenge(metaclass=ABCMeta):
    def __init__(self):
        self._solution = None

    @classmethod
    @abstractmethod
    def id(cls) -> str:
        pass

    def solve(self):
        NUM_EXECUTIONS_TO_MEASURE_EXECUTION_TIME = 1
        execution_time = timeit(
            self._solve, number=NUM_EXECUTIONS_TO_MEASURE_EXECUTION_TIME
        )

        print(f"Execution time: {execution_time:.6f} seconds")
        self.print_solution()

    @abstractmethod
    def _solve(self):
        pass

    def set_solution(self, solution_part1, solution_part2):
        """This method needs to be called by the implementation of _solve()"""
        self._solution = DaySolutionDTO(str(solution_part1), str(solution_part2))

    @property
    def solution_part1(self):
        return self._solution.solution_part1

    @property
    def solution_part2(self):
        return self._solution.solution_part2

    def print_solution(self):
        if not self._solution:
            raise ValueError(
                "Method solve() needs to be called before calling print_solution()"
            )

        self._print_solution()

    def _print_solution(self):
        print(f"Solution: ")
        print(f"- part 1: The answer is {self.get_solution_part1()}")
        print(f"- part 2: The answer is {self.get_solution_part2()}")
