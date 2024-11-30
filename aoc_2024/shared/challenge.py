from abc import abstractmethod, ABCMeta
from timeit import timeit


class Challenge(metaclass=ABCMeta):
    def __init__(self):
        pass

    def solve(self):
        NUM_EXECUTIONS_TO_MEASURE_EXECUTION_TIME = 1
        execution_time = timeit(
            self._solve, number=NUM_EXECUTIONS_TO_MEASURE_EXECUTION_TIME
        )

        print(f"Execution time: {execution_time:.6f} seconds")
        print(f"Solution: ", end="")
        self.print_solution()

    @abstractmethod
    def _solve(self):
        pass

    @abstractmethod
    def print_solution(self):
        pass

    @classmethod
    @abstractmethod
    def id(cls):
        pass
