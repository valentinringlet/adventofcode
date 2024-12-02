import os.path

import numpy as np
import pandas as pd

from shared.challenge import DaySolutionDTO, Challenge


class ChallengeDay02(Challenge):
    def __init__(self):
        super().__init__()

    @classmethod
    def id(cls):
        return "Day2"

    def _solve(self):
        # 1. read input data
        input_data = self.parse_input_data()

        # 2. compute the solution
        num_valid_levels = sum([self.__is_valid_level(level) for level in input_data])

        # 3. set the solution
        self.set_solution(DaySolutionDTO(str(num_valid_levels), "not solved yet"))

    @staticmethod
    def parse_input_data() -> list[list[int]]:
        input_file = "input_day02.txt"
        input_file_path = os.path.join(os.path.dirname(__file__), input_file)

        with open(input_file_path, "r") as file:
            lines = file.readlines()
            stripped_lines = [line.strip() for line in lines]
            valid_lines = [line for line in stripped_lines if line != ""]
            nums = [[int(item) for item in line.split()] for line in valid_lines]
        return nums

    @staticmethod
    def __is_valid_level(level: list[int]) -> bool:
        pairs = [(level[i], level[i + 1]) for i in range(0, len(level) - 1)]
        differences = [first - second for first, second in pairs]

        # 1. Make sure that the numbers are all increasing or all decreasing
        all_diffs_positive = all([diff >= 0 for diff in differences])
        all_diffs_negative = all([diff <= 0 for diff in differences])
        if not all_diffs_positive and not all_diffs_negative:
            return False
        # 2. Make sure subsequent numbers differ by at least 1 and at most 3
        abs_diffs = [abs(diff) for diff in differences]
        return all([1 <= diff <= 3 for diff in abs_diffs])

    def _print_solution(self):
        solution = self.get_solution()
        print(
            f"- part 1: There are {solution.solution_part1} valid levels in the input"
        )
