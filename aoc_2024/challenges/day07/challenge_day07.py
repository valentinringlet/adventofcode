from shared.challenge import Challenge, DaySolutionDTO


class ChallengeDay07(Challenge):
    @classmethod
    def id(cls) -> str:
        return "Day7"

    def _solve(self):
        # TODO
        self.set_solution(DaySolutionDTO("not solved yet", "not solved yet"))

    def _print_solution(self):
        solution = self.get_solution()
        print(f"- part 1: {solution.solution_part1}")
        print(f"- part 2: {solution.solution_part2}")
