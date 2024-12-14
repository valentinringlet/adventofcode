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

        # solve part 1
        num_blinks = 25
        curr_stones = starting_stones.copy()
        for i in range(num_blinks):
            next_stones = []
            for stone in curr_stones:
                if stone == "0":
                    next_stones.append("1")
                elif len(stone) % 2 == 0:
                    first_stone, second_stone = self._split_stone_in_two(stone)
                    next_stones.append(first_stone)
                    next_stones.append(second_stone)
                else:
                    new_stone = str(int(stone) * 2024)
                    next_stones.append(new_stone)

            curr_stones = next_stones
        solution_part1 = len(curr_stones)

        self.set_solution(solution_part1, "not solved yet")

    @staticmethod
    def _split_stone_in_two(stone: str) -> tuple[str, str]:
        middle_idx = len(stone) // 2
        first_half = stone[:middle_idx]
        second_half = stone[middle_idx:]

        # make sure to drop extra leading zeroes
        while len(first_half) > 1 and first_half[0] == "0":
            first_half = first_half[1:]
        while len(second_half) > 1 and second_half[0] == "0":
            second_half = second_half[1:]

        return first_half, second_half
