import os

from shared.challenge import Challenge


class ChallengeDay12(Challenge):
    @classmethod
    def id(cls) -> str:
        return "Day12-workinprogress"

    def _solve(self):
        # parse input
        input_file_name = "input_day12.txt"
        input_file_path = os.path.join(os.path.dirname(__file__), input_file_name)
        with open(input_file_path, "r") as file:
            garden_map = [
                [plot.strip() for plot in line.strip() if line.strip() != ""]
                for line in file.readlines()
            ]

        # solve part 1
        regions = []
        all_plots_to_expand_to_region = [
            (x, y) for y in range(len(garden_map)) for x in range(len(garden_map[y]))
        ]
        while len(all_plots_to_expand_to_region) > 0:
            next_plot = all_plots_to_expand_to_region[0]

            # Expand to all connected plots of the same type
            new_region = [next_plot]
            remaining_to_explore = [next_plot]
            while len(remaining_to_explore) > 0:
                plot_to_explore = remaining_to_explore.pop(0)
                curr_x, curr_y = plot_to_explore
                same_region_neighbours = [
                    (x, y)
                    for x, y in self._get_neighbours_in_bounds(
                        plot_to_explore, garden_map
                    )
                    if garden_map[y][x] == garden_map[curr_y][curr_x]
                ]
                undiscovered_same_region_neighbours = [
                    plot for plot in same_region_neighbours if plot not in new_region
                ]

                remaining_to_explore.extend(undiscovered_same_region_neighbours)
                new_region.extend(undiscovered_same_region_neighbours)

            # Remove all of these plots from the remaining plots to explore
            for plot in new_region:
                all_plots_to_expand_to_region.remove(plot)
            plant_type = garden_map[next_plot[1]][next_plot[0]]
            regions.append((new_region, plant_type))

        fence_price_part1 = 0
        for region_info in regions:
            region_plots, region_type = region_info
            region_area = len(region_plots)
            region_perimeter = self._compute_region_perimeter(region_plots, garden_map)

            fence_price_part1 += region_area * region_perimeter

        self.set_solution(fence_price_part1, "not solved yet")

    def _compute_region_perimeter(
        self, region_plots: list[tuple[int, int]], garden_map: list[list[str]]
    ) -> int:
        region_perimeter = 0
        for plot in region_plots:
            plot_x, plot_y = plot
            other_region_neighbours = [
                (x, y)
                for x, y in self._get_all_neighbours(plot)
                if not self._is_pos_in_bounds((x, y), garden_map)
                or garden_map[plot_y][plot_x] != garden_map[y][x]
            ]
            region_perimeter += len(other_region_neighbours)

        return region_perimeter

    def _get_neighbours_in_bounds(
        self, pos: tuple[int, int], terrain_map: list[list[str]]
    ) -> list[tuple[int, int]]:
        neighbours = []
        all_neighbours = self._get_all_neighbours(pos)
        for neighbour in all_neighbours:
            if self._is_pos_in_bounds(neighbour, terrain_map):
                neighbours.append(neighbour)

        return neighbours

    @staticmethod
    def _is_pos_in_bounds(pos: tuple[int, int], terrain_map: list[list[str]]) -> bool:
        x, y = pos
        return 0 <= y < len(terrain_map) and 0 <= x < len(terrain_map[y])

    @staticmethod
    def _get_all_neighbours(pos: tuple[int, int]) -> list[tuple[int, int]]:
        x, y = pos
        return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
