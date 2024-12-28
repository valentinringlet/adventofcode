import os
import re
from collections import defaultdict
from functools import reduce
from operator import mul

from shared.challenge import Challenge


INPUT_REGEX = "p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)"


class ChallengeDay14(Challenge):
    @classmethod
    def id(cls) -> str:
        return "Day14-WIP"

    def _solve(self):
        # parse the input
        input_file_name = "input_day14.txt"
        WIDTH = 101
        HEIGHT = 103

        input_file_path = os.path.join(os.path.dirname(__file__), input_file_name)
        with open(input_file_path, "r") as file:
            raw_input = [
                line.strip() for line in file.readlines() if line.strip() != ""
            ]
        all_robots = []
        for line in raw_input:
            match = re.fullmatch(INPUT_REGEX, line)
            if not match:
                raise ValueError(
                    f"Invalid input data in input file '{input_file_name}'"
                )
            pos_x, pos_y, v_x, v_y = match.groups()
            all_robots.append(((int(pos_x), int(pos_y)), (int(v_x), int(v_y))))

        # solve part 1
        positions_after_n_seconds_part1 = []
        num_seconds_part1 = 100
        for robot in all_robots:
            # unpack the data
            pos, velocity = robot
            x, y = pos
            v_x, v_y = velocity

            new_x = (x + num_seconds_part1 * v_x) % WIDTH
            new_y = (y + num_seconds_part1 * v_y) % HEIGHT
            positions_after_n_seconds_part1.append((new_x, new_y))

        """ QUADRANT SPLIT:
             1 | 3 
            -------
             2 | 4
        """
        quadrant_counts_part1 = defaultdict(int)
        for pos in positions_after_n_seconds_part1:
            x, y = pos
            if x == WIDTH // 2 or y == HEIGHT // 2:
                # position in the center
                continue
            elif x < WIDTH // 2:
                if y < HEIGHT // 2:
                    quadrant = 1
                else:
                    quadrant = 2
            else:
                if y < HEIGHT // 2:
                    quadrant = 3
                else:
                    quadrant = 4

            quadrant_counts_part1[quadrant] += 1

        solution_part1 = reduce(
            mul,
            [
                value
                for key, value in quadrant_counts_part1.items()
                if key in [1, 2, 3, 4]
            ],
            1,
        )

        self.set_solution(solution_part1, "not solved yet")
