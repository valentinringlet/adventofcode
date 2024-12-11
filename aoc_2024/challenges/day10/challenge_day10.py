import os

from shared.challenge import Challenge


TRAILHEAD = 0


class ChallengeDay10(Challenge):
    @classmethod
    def id(cls) -> str:
        return "Day10"

    def _solve(self):
        # parse the input data
        input_file_name = "input_day10.txt"
        input_file_path = os.path.join(os.path.dirname(__file__), input_file_name)
        with open(input_file_path, "r") as file:
            terrain_map = [
                [char for char in line.strip()]
                for line in file.readlines()
                if line.strip() != ""
            ]

        # solve part 1
        sum_trailhead_scores = 0
        trailhead_positions = [
            (x, y)
            for y in range(len(terrain_map))
            for x in range(len(terrain_map[y]))
            if terrain_map[y][x] == str(TRAILHEAD)
        ]
        for trailhead_pos in trailhead_positions:
            reachable_max_height_positions = set()
            positions_to_explore = [(trailhead_pos, TRAILHEAD)]

            while len(positions_to_explore) != 0:
                curr_pos, curr_height = positions_to_explore.pop(0)

                if curr_height == 9:
                    reachable_max_height_positions.add(curr_pos)
                else:
                    # add all surrounding nodes with the height + 1 to the list to explore
                    next_height = curr_height + 1
                    positions_to_explore.extend(
                        [
                            ((x, y), next_height)
                            for (x, y) in self.get_adjacent_positions(
                                curr_pos, terrain_map
                            )
                            if terrain_map[y][x] == str(next_height)
                        ]
                    )

            trailhead_score = len(reachable_max_height_positions)
            sum_trailhead_scores += trailhead_score

        self.set_solution(sum_trailhead_scores, "not solved yet")

    @staticmethod
    def get_adjacent_positions(
        pos: tuple[int, int], terrain_map: list[list[str]]
    ) -> list[tuple[int, int]]:
        adjacent_positions = []
        x, y = pos
        if y > 0:
            adjacent_positions.append((x, y - 1))
        if y < len(terrain_map) - 1:
            adjacent_positions.append((x, y + 1))
        if x > 0:
            adjacent_positions.append((x - 1, y))
        if x < len(terrain_map[0]) - 1:
            adjacent_positions.append((x + 1, y))

        return adjacent_positions
