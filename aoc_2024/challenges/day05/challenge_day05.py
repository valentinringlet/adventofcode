from shared.challenge import Challenge, DaySolutionDTO


class ChallengeDay05(Challenge):
    @classmethod
    def id(cls) -> str:
        return "Day5"

    def _solve(self):
        # TODO solve the challenge
        self.set_solution(DaySolutionDTO("not solved yet", "not solved yet"))

    def _print_solution(self):
        solution = self.set_solution(DaySolutionDTO)
        # TODO: write what the answer represents
        print(f"- part 1: {solution.solution_part2}")
        print(f"- part 2: {solution.solution_part2}")
