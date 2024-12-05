from shared.challenge import Challenge, DaySolutionDTO


class ChallengeDay04(Challenge):
    @classmethod
    def id(cls) -> str:
        return "Day4"

    def _solve(self):
        self.set_solution(DaySolutionDTO("not solved yet", "not solved yet"))

    def _print_solution(self):
        solution = self.get_solution()
        print("Nothing is solved yet")
