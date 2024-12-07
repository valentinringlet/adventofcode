import os
import operator

from shared.challenge import Challenge, DaySolutionDTO


class ChallengeDay07(Challenge):
    @classmethod
    def id(cls) -> str:
        return "Day7"

    def _solve(self):
        # 1. read input data
        input_file = "input_day07.txt"  # "test_input.txt"
        input_file_path = os.path.join(os.path.dirname(__file__), input_file)
        all_equations = self._parse_input(input_file_path)

        # 2. solve part 1
        # 2.1. find the equations that could possibly be true
        valid_equations = []
        for equation in all_equations:
            result_value, factors = equation
            start_value, remaining_factors = factors[0], factors[1:]
            if self._can_factors_make_target(
                start_value, remaining_factors, result_value
            ):
                valid_equations.append(equation)
        # 2.2. compute the solution of part 1
        solution_part1 = sum(
            [result_value for result_value, factors in valid_equations]
        )

        self.set_solution(DaySolutionDTO(str(solution_part1), "not solved yet"))

        self.set_solution(solution_part1, solution_part2)

    @staticmethod
    def _parse_input(file_path: str) -> list[tuple[int, tuple[int, ...]]]:
        with open(file_path, "r") as file:
            all_equations_str = [
                line.strip().split(":")
                for line in file.readlines()
                if line.strip() != ""
            ]
            all_equations = [
                (int(result), tuple([int(num) for num in factors.strip().split()]))
                for result, factors in all_equations_str
            ]
            return all_equations

    def _can_factors_make_target(
        self, current_value: int, factors: tuple[int, ...], target_value: int
    ) -> bool:
        if len(factors) == 0:
            if current_value == target_value:
                return True
            else:
                return False
        else:
            for operation in [operator.add, operator.mul]:
                if self._can_factors_make_target(
                    operation(current_value, factors[0]), factors[1:], target_value
                ):
                    return True
            return False
