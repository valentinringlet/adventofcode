from abc import abstractmethod, ABCMeta
from timeit import timeit


class Challenge(metaclass=ABCMeta):
    def __init__(self):
        self._solution = None

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

    def set_solution(self, solution):
        """ This method needs to be called by the implementation of _solve()
        """
        self._solution = solution

    def get_solution(self):
        return self._solution

    def print_solution(self):
        if not self._solution:
            raise ValueError(
                "Method solve() needs to be called before calling get_solution()"
            )

        self._print_solution()

    @abstractmethod
    def _print_solution(self):
        pass

    @classmethod
    @abstractmethod
    def id(cls):
        pass
