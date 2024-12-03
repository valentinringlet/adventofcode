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

        non_ignored_mul_instructions = []
        ignored_range_idx = 0
        ignored_range_start, ignored_range_end = ignored_mul_instruction_ranges[
            ignored_range_idx
        ]
        for mul_idx, mul_params in mul_instruction_info:
            # Fast-forward to the relevant ignored range
            while mul_idx > ignored_range_end and ignored_range_idx < len(
                ignored_mul_instruction_ranges
            ):
                ignored_range_idx += 1
                if ignored_range_idx == len(ignored_mul_instruction_ranges):
                    ignored_range_start = len(input_data)
                    ignored_range_end = ignored_range_start
                else:
                    (
                        ignored_range_start,
                        ignored_range_end,
                    ) = ignored_mul_instruction_ranges[ignored_range_idx]

            if not (ignored_range_start < mul_idx < ignored_range_end):
                # this mul is not ignored
                first_param, second_param = mul_params
                non_ignored_mul_instructions.append((first_param, second_param))

        return sum(
            [
                int(first_param) * int(second_param)
                for first_param, second_param in non_ignored_mul_instructions
            ]
        )

    def _print_solution(self):
        solution = self.get_solution()
        print(
            f"- part 1: The result of the valid mul instructions is {solution.solution_part1}"
        )
        print(
            f"- part 2: The result of the valid mul instructions which are not disabled is {solution.solution_part2}"
        )
