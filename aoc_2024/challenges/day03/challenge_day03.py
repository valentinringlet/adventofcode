import os
import re

from shared.challenge import Challenge, DaySolutionDTO


class ChallengeDay03(Challenge):
    def __init__(self):
        super().__init__()

    @classmethod
    def id(cls) -> str:
        return "Day3"

    def _solve(self):
        # 1. read input data
        input_file = "input_day03.txt"  # "test_input.txt"
        input_file_path = os.path.join(os.path.dirname(__file__), input_file)
        input_data = self.parse_input_data(input_file_path)

        # 2. compute solution
        solution_part1 = self._solve_part1(input_data)

        # 3. set solution
        self.set_solution(DaySolutionDTO(str(solution_part1), "not solved yet"))

    @staticmethod
    def parse_input_data(input_file_path) -> str:
        with open(input_file_path, "r") as file:
            return "".join([line.strip() for line in file.readlines()])

    @staticmethod
    def _solve_part1(input_data: str):
        mul_instruction_regex = r"mul\((\d+),(\d+)\)"
        mul_instructions = re.findall(mul_instruction_regex, input_data)
        return sum(
            [
                int(first_param) * int(second_param)
                for first_param, second_param in mul_instructions
            ]
            second_parameter = input_data[next_comma_idx + 1 : next_bracket_idx]
            if not first_parameter.isnumeric() or not second_parameter.isnumeric():
                i = next_mul_start_idx + 1
                continue

            # we found a valid instruction
            valid_mul_instructions.append((int(first_parameter), int(second_parameter)))
            i = next_bracket_idx + 1

    def _print_solution(self):
        solution = self.get_solution()
        print(
            f"- part 1: The result of the valid mul instructions is {solution.solution_part1}"
        )
