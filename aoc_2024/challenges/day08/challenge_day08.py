import os

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
        valid_antinodes = set()
        for freq in all_frequencies:
            pos_nodes = [
                (x, y)
                for y in range(len(signal_map))
                for x in range(len(signal_map[y]))
                if signal_map[y][x] == freq
            ]
            for i in range(len(pos_nodes)):
                curr_x, curr_y = pos_nodes[i]
                for other_x, other_y in pos_nodes[i + 1 :]:
                    pos_diff_x, pos_diff_y = (curr_x - other_x, curr_y - other_y)

                    antinode1 = (curr_x + pos_diff_x, curr_y + pos_diff_y)
                    antinode2 = (other_x - pos_diff_x, other_y - pos_diff_y)
                    for possible_antinode in [antinode1, antinode2]:
                        if self._is_pos_within_map_bounds(
                            possible_antinode, signal_map
                        ):
                            valid_antinodes.add(possible_antinode)

        num_antinodes = len(valid_antinodes)

        # PROBLEM: answer is too high
        self.set_solution(num_antinodes, "not solved yet")

    @staticmethod
    def _parse_input_data(file_path: str) -> list[list[str]]:
        with open(file_path, "r") as file:
            return [
                [char for char in line.strip()]
                for line in file.readlines()
                if line.strip() != ""
            ]

    @staticmethod
    def _is_pos_within_map_bounds(
        pos: tuple[int, int], signal_map: list[list[str]]
    ) -> bool:
        x, y = pos
        return 0 <= y <= len(signal_map) and 0 <= x <= len(signal_map[0])

    def _show_map(self, signal_map: list[list[str]]):
        for row in signal_map:
            for char in row:
                print(char, end="")
            print()
