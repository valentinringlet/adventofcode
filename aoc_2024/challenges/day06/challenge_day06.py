import os
from enum import Enum
from typing import Callable

from shared.challenge import Challenge, DaySolutionDTO

GUARD_SYMBOL = "^"


# IMPORTANT: the directions are ordered such that each next direction is +90 degrees compared to the previous one
class Direction(Enum):
    UP: int = 0
    RIGHT: int = 1
    DOWN: int = 2
    LEFT: int = 3

    def turn_90_degrees_clockwise(self):
        return Direction((self.value + 1) % len(Direction))


class ChallengeDay06(Challenge):
    @classmethod
    def id(cls) -> str:
        return "Day6"

    def _solve(self):
        # 1. read input data
        input_file = "input_day06.txt"  # "test_input_part1.txt"
        input_file_path = os.path.join(os.path.dirname(__file__), input_file)
        input_data = self.parse_input(input_file_path)

        # 2. solve the challenge
        solution_part1 = self._solve_part1(input_data)

        # 3. set the solution
        self.set_solution(DaySolutionDTO(str(solution_part1), "not solved yet"))

    def _print_solution(self):
        solution = self.get_solution()
        print(
            f"- part 1: The guard will visit {solution.solution_part1} different positions on the map"
        )
        print(f"- part 2: {solution.solution_part2}")

    @staticmethod
    def parse_input(file_path: str) -> list[list[str]]:
        with open(file_path, "r") as file:
            return [
                list(line.strip()) for line in file.readlines() if line.strip() != ""
            ]

    def _solve_part1(self, input_data: list[list[str]]) -> int:
        guard_start_pos = self._get_guard_starting_position(input_data)

        all_guard_positions = [
            [False for _ in range(len(input_data[y]))] for y in range(len(input_data))
        ]
        start_x, start_y = guard_start_pos
        all_guard_positions[start_y][start_x] = True

        current_pos = guard_start_pos
        current_dir = Direction.UP
        exited_map = False
        while not exited_map:
            # Move once in current direction
            new_dir = current_dir
            new_pos = self._move_one_step_from_pos_in_dir(current_pos, new_dir)
            new_x, new_y = new_pos

            if self._is_position_within_map_bounds(new_pos, input_data):
                # Act based on what object we would walk into next
                match input_data[new_y][new_x]:
                    case "#":
                        # Guard is blocked, instead of moving forward we turn 90 degrees + move in that direction
                        new_dir = current_dir.turn_90_degrees_clockwise()
                        new_pos = self._move_one_step_from_pos_in_dir(
                            current_pos, new_dir
                        )
                        new_x, new_y = new_pos
                    case _:
                        # otherwise, we just continue straight ahead
                        pass

                # Move to the next position
                current_pos = new_pos
                current_dir = new_dir
                all_guard_positions[new_y][new_x] = True
            else:
                exited_map = True

        num_guard_positions = sum(
            [sum([int(x) for x in row]) for row in all_guard_positions]
        )

        return num_guard_positions

    @staticmethod
    def _get_guard_starting_position(input_data: list[list[str]]):
        guard_positions = [
            (x, y)
            for y in range(len(input_data))
            for x in range(len(input_data[y]))
            if input_data[y][x] == GUARD_SYMBOL
        ]
        if len(guard_positions) > 1:
            raise ValueError(
                "The guard is at more than 1 position in the starting layout"
            )
        guard_start_pos = guard_positions[0]
        return guard_start_pos

    @staticmethod
    def _is_position_within_map_bounds(
        position: tuple[int, int], input_data: list[list[str]]
    ) -> bool:
        x, y = position
        return 0 <= y < len(input_data) and 0 <= x < len(input_data[0])

    @staticmethod
    def _move_one_step_from_pos_in_dir(
        position: tuple[int, int], direction: Direction
    ) -> tuple[int, int]:
        x, y = position
        match direction:
            case Direction.UP:
                return x, y - 1
            case Direction.RIGHT:
                return x + 1, y
            case Direction.DOWN:
                return x, y + 1
            case Direction.LEFT:
                return x - 1, y

    @staticmethod
    def _move_one_step_in_dir(
        direction: Direction,
    ) -> Callable[[tuple[int, int]], tuple[int, int]]:
        match direction:
            case Direction.UP:
                return lambda pos: (pos[0], pos[1] - 1)
            case Direction.RIGHT:
                return lambda pos: (pos[0] + 1, pos[1])
            case Direction.DOWN:
                return lambda pos: (pos[0], pos[1] + 1)
            case Direction.LEFT:
                return lambda pos: (pos[0] - 1, pos[1])

    @staticmethod
    def _show_pos_on_map(pos: tuple[int, int], input_data: list[list[str]]):
        for y in range(len(input_data)):
            for x in range(len(input_data[y])):
                if x == pos[0] and y == pos[1]:
                    print("x", end="")
                else:
                    print(input_data[y][x], end="")
            print()
        print()
