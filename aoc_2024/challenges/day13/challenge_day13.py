import os
import re
from typing import Optional

from shared.challenge import Challenge


button_a_regex = "Button A: X\+(\d+), Y\+(\d+)"
button_b_regex = "Button B: X\+(\d+), Y\+(\d+)"
target_regex = "Prize: X=(\d+), Y=(\d+)"


class ChallengeDay13(Challenge):
    @classmethod
    def id(cls) -> str:
        return "Day13"

    def _solve(self):
        # read input file
        input_file_name = "input_day13.txt"
        input_file_path = os.path.join(os.path.dirname(__file__), input_file_name)
        with open(input_file_path, "r") as file:
            raw_input = [line.strip() for line in file.readlines()]

        # solve part 1
        token_cost_button_a = 3
        token_cost_button_b = 1
        num_tokens_required_part1 = 0
        num_tokens_required_part2 = 0
        for i in range(len(raw_input)):
            button_a_match = re.match(button_a_regex, raw_input[i])
            if button_a_match:
                button_a = tuple([int(coord) for coord in button_a_match.groups()])
                button_b = tuple(
                    [
                        int(coord)
                        for coord in re.match(button_b_regex, raw_input[i + 1]).groups()
                    ]
                )
                target = tuple(
                    [
                        int(coord)
                        for coord in re.match(target_regex, raw_input[i + 2]).groups()
                    ]
                )
                if len(button_a) != 2 or len(button_b) != 2 or len(target) != 2:
                    raise ValueError("Input does not match required structure")
                else:
                    # solve part 1
                    x_a, y_a = button_a
                    x_b, y_b = button_b
                    x_target, y_target = target

                    solution = self.solve_2_equations_with_2_unknowns(
                        equation1=(x_a, x_b, x_target), equation2=(y_a, y_b, y_target)
                    )
                    if solution:
                        num_button_a_pressed, num_button_b_pressed = solution
                        cost = (
                            int(num_button_a_pressed) * token_cost_button_a
                            + int(num_button_b_pressed) * token_cost_button_b
                        )
                        num_tokens_required_part1 += cost

                    # solve part 2
                    added = 10000000000000
                    x_target += added
                    y_target += added

                    solution = self.solve_2_equations_with_2_unknowns(
                        equation1=(x_a, x_b, x_target), equation2=(y_a, y_b, y_target)
                    )
                    if solution:
                        num_button_a_pressed, num_button_b_pressed = solution
                        cost = (
                            int(num_button_a_pressed) * token_cost_button_a
                            + int(num_button_b_pressed) * token_cost_button_b
                        )
                        num_tokens_required_part2 += cost

        self.set_solution(num_tokens_required_part1, num_tokens_required_part2)

    @staticmethod
    def solve_2_equations_with_2_unknowns(
            equation1: tuple[int, int, int], equation2: tuple[int, int, int]
    ) -> Optional[tuple[int, int]]:
        # unpack equations
        x_a, x_b, x_target = equation1
        y_a, y_b, y_target = equation2

        """
        HOW TO GET SOLUTION?
        ------------------------
        We have a system of 2 equations with 2 unknowns:
            1. x_a * n_a + x_b * n_b = x_target (3)
            2. y_a * n_a + y_b * n_b = y_target (2)

        Solution:
            n_a = (x_target - x_b * n_b)/x_a (2)

            Inserting (2) into (1):
            y_a * (x_target - x_b * n_b)/x_a + y_b * n_b = y_target
        <=> y_a * x_target/x_a - y_a * x_b * n_b/x_a + y_b * n_b = y_target
        <=> n_b * (y_b - y_a * x_b/x_a) = y_target - y_a * x_target/x_a
        <=> n_b = (y_target - y_a * x_target/x_a) / (y_b - y_a * x_b/x_a)
                = (y_target * x_a - y_a * x_target)/x_a * x_a/(y_b * x_a - y_a * x_b)
                = (y_target * x_a - y_a * x_target)/(y_b * x_a - y_a * x_b) (4)

            Inserting (4) into (3):
            x_a * n_a + x_b * (y_target * x_a - y_a * x_target)/(y_b * x_a - y_a * x_b) = x_target
        <=> x_a * n_a = [(x_target * y_b * x_a - x_target * y_a * x_b) - (x_b * y_target * x_a - x_b * y_a * x_target)] 
                            / (y_b * x_a - y_a * x_b)
        <=> n_a = (x_target * y_b * x_a - y_target * x_b * x_a) / [x_a * (y_b * x_a - y_a * x_b)]
                = (x_target * y_b - y_target * x_b)/(y_b * x_a - y_a * x_b)
        """

        # solve them (details on how to establish solution equations below)
        denominator = y_b * x_a - y_a * x_b
        if denominator != 0:
            coeff_a = (x_target * y_b - y_target * x_b) / denominator
            coeff_b = (y_target * x_a - x_target * y_a) / denominator

            if coeff_a.is_integer() and coeff_b.is_integer():
                return int(coeff_a), int(coeff_b)

        # if any condition is not fulfilled, there is no solution
        return None
