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
        input_file = "input_day02.txt"  # "test_input.txt"
        input_file_path = os.path.join(os.path.dirname(__file__), input_file)
        input_data = self.parse_input_data(input_file_path)

        # 2. compute the solution
        num_valid_levels_part1 = sum(
            [self.__is_valid_level_part1(level) for level in input_data]
        )

        # 3. set the solution
        self.set_solution(DaySolutionDTO(str(num_valid_levels_part1), "not solved yet"))

    @staticmethod
    def parse_input_data(input_file_path: str) -> list[list[int]]:
        with open(input_file_path, "r") as file:
            lines = file.readlines()
            stripped_lines = [line.strip() for line in lines]
            valid_lines = [line for line in stripped_lines if line != ""]
            nums = [[int(item) for item in line.split()] for line in valid_lines]
        return nums

    def __is_valid_level_part1(self, level: list[int]) -> bool:
        level_is_all_increasing = self.__is_level_fully_increasing(level)
        level_is_all_decreasing = self.__is_level_fully_decreasing(level)
        level_has_increases_in_range = self.__level_has_increases_and_decreases_in_range(
            level, lower_bound=1, upper_bound=3
        )

        return (
            level_is_all_increasing or level_is_all_decreasing
        ) and level_has_increases_in_range

    @staticmethod
    def __is_level_fully_increasing(level: list[int]) -> bool:
        return all([level[i + 1] - level[i] >= 0 for i in range(len(level) - 1)])

    def __is_level_fully_decreasing(self, level: list[int]) -> bool:
        return self.__is_level_fully_increasing([-elem for elem in level])

    @staticmethod
    def __level_has_increases_and_decreases_in_range(
        level: list[int], lower_bound: int = 1, upper_bound: int = 3
    ) -> bool:
        abs_differences = [abs(level[i + 1] - level[i]) for i in range(len(level) - 1)]
        return all([lower_bound <= diff <= upper_bound for diff in abs_differences])

    def _print_solution(self):
        solution = self.get_solution()
        print(
            f"- part 1: There are {solution.solution_part1} valid levels in the input"
        )
