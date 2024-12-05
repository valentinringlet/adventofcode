import os
import re

from shared.challenge import Challenge, DaySolutionDTO

DISABLE_MUL_INSTRUCTION_REGEX = r"don't\(\)"
ENABLE_MUL_INSTRUCTION_REGEX = r"do\(\)"
MUL_INSTRUCTION_REGEX = r"mul\((\d+),(\d+)\)"


class ChallengeDay03(Challenge):
    def __init__(self):
        super().__init__()

    @classmethod
    def id(cls) -> str:
        return "Day3"

    def _solve(self):
        # 1. read input data
        input_file = "input_day03.txt"
        input_file_path = os.path.join(os.path.dirname(__file__), input_file)
        input_data = self.parse_input_data(input_file_path)

        # 2. compute solution
        solution_part1 = self._solve_part1(input_data)
        solution_part2 = self._solve_part2(input_data)

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

    @staticmethod
    def _solve_part2(input_data: str) -> int:
        mul_instructions = [
            (match.start(), "MUL", match.groups())
            for match in re.finditer(MUL_INSTRUCTION_REGEX, input_data)
        ]
        disable_mul_instructions = [
            (match.start(), "DONT")
            for match in re.finditer(DISABLE_MUL_INSTRUCTION_REGEX, input_data)
        ]
        enable_mul_instructions = [
            (match.start(), "DO")
            for match in re.finditer(ENABLE_MUL_INSTRUCTION_REGEX, input_data)
        ]

        # Make a list of all instructions ordered by the index at which they occur
        all_instructions = (
            mul_instructions + disable_mul_instructions + enable_mul_instructions
        )
        all_instructions.sort(key=lambda instruction: instruction[0])

        # Make a state machine iterate over the instructions
        mul_enabled = True
        valid_mul_instructions = []
        for instruction in all_instructions:
            instruction_type = instruction[1]
            match instruction_type:
                case "DO":
                    mul_enabled = True
                case "DONT":
                    mul_enabled = False
                case "MUL":
                    if mul_enabled:
                        first_param, second_param = instruction[2]
                        valid_mul_instructions.append((int(first_param), int(second_param)))

        return sum(
            [
                first_param * second_param
                for first_param, second_param in valid_mul_instructions
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
