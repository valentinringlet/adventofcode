import os
from dataclasses import dataclass

import pandas as pd

from shared.challenge import Challenge, DaySolutionDTO


@dataclass
class Day1Input:
    left_list: list[int]
    right_list: list[int]


class ChallengeDay01(Challenge):
    def __init__(self):
        super().__init__()
        self._sum_of_differences = None

    @classmethod
    def id(cls):
        return "Day1"

    def _solve(self):
        # 1. read the input data
        input_data = self.parse_input_data()

        # 2. solve part 1
        left_sorted_list = sorted(input_data.left_list)
        right_sorted_list = sorted(input_data.right_list)
        differences = [
            abs(left - right)
            for left, right in zip(left_sorted_list, right_sorted_list)
        ]
        sum_of_diffs = sum(differences)
        solution_part1 = sum_of_diffs

        # 3. solve part 2
        similarity_score = 0
        for left_num in input_data.left_list:
            num_occurrences_in_right_list = input_data.right_list.count(left_num)
            similarity_score += left_num * num_occurrences_in_right_list
        solution_part2 = similarity_score

        # 4. save solution
        self.set_solution(DaySolutionDTO(str(solution_part1), str(solution_part2)))

    @staticmethod
    def parse_input_data() -> Day1Input:
        input_file_name = "input_day01.txt"
        input_file_path = os.path.join(
            os.path.realpath(os.path.dirname(__file__)), input_file_name
        )
        with open(input_file_path, "r") as file:
            data = pd.read_csv(file, sep="\s+", header=None)
            left_list: list[int] = data.iloc[:, 0].to_list()
            right_list: list[int] = data.iloc[:, 1].to_list()

        return Day1Input(left_list, right_list)

    def _print_solution(self):
        solution = self.get_solution()
        print(
            f"- part 1: The sum of differences of the items in the two lists is {solution.solution_part1}"
        )
        print(
            f"- part 2: The similarity score of the two lists is {solution.solution_part2}"
        )
