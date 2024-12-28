import os
import re

from shared.challenge import Challenge


button_a_regex = "Button A: X\+(\d+), Y\+(\d+)"
button_b_regex = "Button B: X\+(\d+), Y\+(\d+)"
target_regex = "Prize: X=(\d+), Y=(\d+)"


class ChallengeDay13(Challenge):
    @classmethod
    def id(cls) -> str:
        return "Day13-workinprogress"

    def _solve(self):
        # read input file
        input_file_name = "input_day13.txt"
        input_file_path = os.path.join(os.path.dirname(__file__), input_file_name)
        with open(input_file_path, "r") as file:
            raw_input = [line.strip() for line in file.readlines()]

        # solve part 1
        token_cost_button_a = 3
        token_cost_button_b = 1
        num_tokens_required = 0
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
                    # all_claw_machines.append(ClawMachine(buttonA, buttonB, target))
                    x_a, y_a = button_a
                    x_b, y_b = button_b
                    x_target, y_target = target

                    """
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
                    denominator = y_b * x_a - y_a * x_b
                    if denominator != 0:
                        num_button_a_pressed = (
                            x_target * y_b - y_target * x_b
                        ) / denominator
                        num_button_b_pressed = (
                            y_target * x_a - x_target * y_a
                        ) / denominator

                        if (
                            num_button_a_pressed.is_integer()
                            and num_button_b_pressed.is_integer()
                        ):
                            cost = (
                                int(num_button_a_pressed) * token_cost_button_a
                                + int(num_button_b_pressed) * token_cost_button_b
                            )
                            num_tokens_required += cost

        self.set_solution(int(num_tokens_required), "not solved yet")
