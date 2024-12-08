import os
from typing import Callable, Iterable

from shared.challenge import Challenge


class ChallengeDay08(Challenge):
    @classmethod
    def id(cls) -> str:
        return "Day8"

    def _solve(self):
        input_file = "input_day08.txt"  # "test_input.txt"
        input_file_path = os.path.join(os.path.dirname(__file__), input_file)
        signal_map = self._parse_input_data(input_file_path)

        all_frequencies = set(
            [
                signal_map[y][x]
                for y in range(len(signal_map))
                for x in range(len(signal_map[y]))
                if signal_map[y][x].isalnum()
            ]
        )
        num_antinodes_part1 = self._get_num_valid_antinodes(
            all_frequencies, signal_map, self._get_antinodes_part1
        )

        # PROBLEM: answer is too high
        self.set_solution(num_antinodes_part1, "not solved yet")

    def _get_num_valid_antinodes(
        self,
        all_frequencies: set[str],
        signal_map: list[list[str]],
        get_antinodes_method: Callable[
            [tuple[int, int], tuple[int, int], list[list[str]]], set[tuple[int, int]]
        ],
    ) -> int:
        valid_antinodes = set()
        for freq in all_frequencies:
            pos_nodes = [
                (x, y)
                for y in range(len(signal_map))
                for x in range(len(signal_map[y]))
                if signal_map[y][x] == freq
            ]
            for i in range(len(pos_nodes)):
                curr_pos = pos_nodes[i]
                for other_pos in pos_nodes[i + 1 :]:
                    antinodes = get_antinodes_method(curr_pos, other_pos, signal_map)
                    valid_antinodes.update(antinodes)
        num_antinodes = len(valid_antinodes)
        return num_antinodes

    @staticmethod
    def _parse_input_data(file_path: str) -> list[list[str]]:
        with open(file_path, "r") as file:
            return [
                [char for char in line.strip()]
                for line in file.readlines()
                if line.strip() != ""
            ]

    def _get_antinodes_part1(
        self,
        node1: tuple[int, int],
        node2: tuple[int, int],
        signal_map: list[list[str]],
    ) -> set[tuple[int, int]]:
        antinodes = set()
        x1, y1 = node1
        x2, y2 = node2

        pos_diff_x, pos_diff_y = (x1 - x2, y1 - y2)

        antinode1 = (x1 + pos_diff_x, y1 + pos_diff_y)
        antinode2 = (x2 - pos_diff_x, y2 - pos_diff_y)
        for possible_antinode in [antinode1, antinode2]:
            if self._is_pos_within_map_bounds(possible_antinode, signal_map):
                antinodes.add(possible_antinode)

        return antinodes

    @staticmethod
    def _is_pos_within_map_bounds(
        pos: Iterable[int], signal_map: list[list[str]]
    ) -> bool:
        x, y = pos
        return 0 <= y < len(signal_map) and 0 <= x < len(signal_map[y])

    def _show_map(self, signal_map: list[list[str]]):
        for row in signal_map:
            for char in row:
                print(char, end="")
            print()
