import os
from dataclasses import dataclass
from enum import Enum, unique, auto

from shared.challenge import Challenge, DaySolutionDTO


@unique
class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    UP_LEFT = auto()
    UP_RIGHT = auto()
    DOWN_LEFT = auto()
    DOWN_RIGHT = auto()


@dataclass
class Move:
    dir: Direction
    pos: tuple[int, int]


class ChallengeDay04(Challenge):
    @classmethod
    def id(cls) -> str:
        return "Day4"

    def _solve(self):
        # 1. read input data
        input_file = "test_input_part1.txt"  # "input_day04.txt"
        input_file_path = os.path.join(os.path.dirname(__file__), input_file)
        input_data = self.parse_input(input_file_path)

        # 2. use input data to find all XMAS'es
        solution_part1 = self._solve_part1_approach1(input_data)

        # 3. set solution
        self.set_solution(DaySolutionDTO(str(solution_part1), "not solved yet"))

    @staticmethod
    def parse_input(file_path: str) -> list[str]:
        with open(file_path, "r") as file:
            return [line.strip() for line in file if line.strip() != ""]

    def _solve_part1_approach1(self, input_data: list[str]):
        all_xmas_occurrences = self._get_all_occurrences_of_target_str(
            input_data, target_str="XMAS"
        )
        solution_part1 = len(all_xmas_occurrences)
        return solution_part1

    def _get_all_occurrences_of_target_str(
        self, input_data: list[str], target_str: str = "XMAS"
    ):
        all_xmas_occurrences = []
        for y in range(len(input_data)):
            for x in range(len(input_data[y])):
                if input_data[y][x] == target_str[0]:
                    # We have a beginning of a match
                    possible_moves = self._get_possible_moves(input_data, x, y)

                    if len(possible_moves) != 0:
                        # Try to match the surrounding positions with the next letter and so forth
                        matches_to_make = [
                            (1, possible_move) for possible_move in possible_moves
                        ]
                        while len(matches_to_make) != 0:
                            next_match = matches_to_make.pop(0)
                            target_str_idx, move = next_match
                            match_x, match_y = move.pos

                            if (
                                input_data[match_y][match_x]
                                == target_str[target_str_idx]
                            ):
                                next_target_str_idx = target_str_idx + 1
                                if next_target_str_idx == len(target_str):
                                    # We have found a complete match!
                                    all_xmas_occurrences.append(move)
                                else:
                                    # We have matched one more letter, but not yet matched the full target string
                                    following_move = self._get_possible_move_in_dir(
                                        input_data, match_x, match_y, move.dir
                                    )
                                    if following_move:
                                        matches_to_make.append(
                                            (next_target_str_idx, following_move)
                                        )

        return all_xmas_occurrences

    @staticmethod
    def _get_possible_moves(input_data: list[str], x: int, y: int) -> list[Move]:
        connected_positions = []
        x_can_decrease = x > 0
        x_can_increase = x < len(input_data[y]) - 1
        y_can_decrease = y > 0
        y_can_increase = y < len(input_data) - 1
        if x_can_decrease:
            connected_positions.append(Move(Direction.LEFT, (x - 1, y)))
        if x_can_increase:
            connected_positions.append(Move(Direction.RIGHT, (x + 1, y)))
        if y_can_decrease:
            connected_positions.append(Move(Direction.UP, (x, y - 1)))
        if y_can_increase:
            connected_positions.append(Move(Direction.DOWN, (x, y + 1)))
        if x_can_decrease and y_can_decrease:
            connected_positions.append(Move(Direction.UP_LEFT, (x - 1, y - 1)))
        if x_can_decrease and y_can_increase:
            connected_positions.append(Move(Direction.UP_RIGHT, (x - 1, y + 1)))
        if x_can_increase and y_can_decrease:
            connected_positions.append(Move(Direction.DOWN_LEFT, (x + 1, y - 1)))
        if x_can_increase and y_can_increase:
            connected_positions.append(Move(Direction.DOWN_RIGHT, (x + 1, y + 1)))

        return connected_positions

    @staticmethod
    def _get_possible_move_in_dir(
        input_data: list[str], x: int, y: int, direction: Direction
    ) -> Move | None:
        x_can_decrease = x > 0
        x_can_increase = x < len(input_data[y]) - 1
        y_can_decrease = y > 0
        y_can_increase = y < len(input_data) - 1
        match direction:
            case Direction.UP:
                if y_can_decrease:
                    return Move(Direction.UP, (x, y - 1))
            case Direction.DOWN:
                if y_can_increase:
                    return Move(Direction.DOWN, (x, y + 1))
            case Direction.LEFT:
                if x_can_decrease:
                    return Move(Direction.LEFT, (x - 1, y))
            case Direction.RIGHT:
                if x_can_increase:
                    return Move(Direction.RIGHT, (x + 1, y))
            case Direction.UP_LEFT:
                if x_can_decrease and y_can_decrease:
                    return Move(Direction.UP_LEFT, (x - 1, y - 1))
            case Direction.UP_RIGHT:
                if x_can_decrease and y_can_increase:
                    return Move(Direction.UP_RIGHT, (x - 1, y + 1))
            case Direction.DOWN_LEFT:
                if x_can_increase and y_can_decrease:
                    return Move(Direction.DOWN_LEFT, (x + 1, y - 1))
            case Direction.DOWN_RIGHT:
                if x_can_increase and y_can_increase:
                    return Move(Direction.DOWN_RIGHT, (x + 1, y + 1))

        return None

    def _print_solution(self):
        solution = self.get_solution()
        print(
            f"- part 1: There are {solution.solution_part1} occurrences of the XMAS in the input"
        )
