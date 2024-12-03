import os
import re

from shared.challenge import Challenge, DaySolutionDTO


IGNORE_MUL_INSTRUCTION = "don't()"
DONT_IGNORE_MUL_INSTRUCTION = "do()"
MUL_INSTRUCTION_REGEX = r"mul\((\d+),(\d+)\)"


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
        solution_part2 = self._solve_part2(input_data)
        # PROBLEM: CURRENT ANSWER FOR PART 2 IS TOO LOW

        # 3. set solution
        self.set_solution(DaySolutionDTO(str(solution_part1), str(solution_part2)))

    @staticmethod
    def parse_input_data(input_file_path) -> str:
        with open(input_file_path, "r") as file:
            return "".join([line.strip() for line in file.readlines()])

    @staticmethod
    def _solve_part1(input_data: str) -> int:
        mul_instructions = re.findall(MUL_INSTRUCTION_REGEX, input_data)
        return sum(
            [
                int(first_param) * int(second_param)
                for first_param, second_param in mul_instructions
            ]
        )

    def _solve_part2(self, input_data: str) -> int:
        ignored_mul_instruction_ranges = [
            (match.start(0), match.start(1))
            for match in re.finditer(r"don't\(\).*(do\(\)?)", input_data)
        ]
        mul_instruction_info = [
            (match.start(), match.groups())
            for match in re.finditer(MUL_INSTRUCTION_REGEX, input_data)
        ]

            # we found a valid instruction
            valid_mul_instructions.append((int(first_parameter), int(second_parameter)))
            i = next_bracket_idx + 1

    def _print_solution(self):
        solution = self.get_solution()
        print(
            f"- part 1: The result of the valid mul instructions is {solution.solution_part1}"
        )
        print(
            f"- part 2: The result of the valid mul instructions which are not disabled is {solution.solution_part2}"
        )
