import os

from shared.challenge import Challenge


class ChallengeDay11(Challenge):
    @classmethod
    def id(cls) -> str:
        return "Day11-not fully solved yet"

    def _solve(self):
        # parse the input data
        input_file_name = "input_day11.txt"  # "test_input_part1.txt"  #
        input_file_path = os.path.join(os.path.dirname(__file__), input_file_name)
        with open(input_file_path, "r") as file:
            starting_stones = [stone.strip() for stone in file.readline().split()]

        # solve parts 1 & 2
        num_blinks_part1 = 25
        num_blinks_part2 = 75
        curr_stones = {stone: 1 for stone in starting_stones}
        solution_part1 = None
        for i in range(num_blinks_part2):
            if i == num_blinks_part1:
                solution_part1 = sum(curr_stones.values())

            archive = {"0": ["1"]}
            next_stones = {}
            for stone, count in curr_stones.items():
                if stone in archive:
                    stones_to_add = archive[stone]
                elif len(stone) % 2 == 0:
                    first_stone, second_stone = self._split_stone_in_two(stone)
                    stones_to_add = [first_stone, second_stone]
                    archive[stone] = stones_to_add
                else:
                    new_stone = str(int(stone) * 2024)
                    stones_to_add = [new_stone]
                    archive[stone] = stones_to_add

                for new_stone in stones_to_add:
                    old_count = (
                        next_stones[new_stone] if new_stone in next_stones else 0
                    )
                    next_stones[new_stone] = old_count + count

            curr_stones = next_stones

        solution_part2 = sum(curr_stones.values())

        self.set_solution(solution_part1, solution_part2)

    @staticmethod
    def _split_stone_in_two(stone: str) -> tuple[str, str]:
        middle_idx = len(stone) // 2
        first_half = stone[:middle_idx]
        second_half = stone[middle_idx:]

        # make sure to drop extra leading zeroes
        cutoff = 0
        while cutoff < len(first_half) - 1 and first_half[cutoff] == "0":
            cutoff += 1
        first_half = first_half[cutoff:]
        cutoff = 0
        while cutoff < len(second_half) - 1 and second_half[cutoff] == "0":
            cutoff += 1
        second_half = second_half[cutoff:]

        return first_half, second_half
