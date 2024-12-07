import os.path

from shared.challenge import Challenge


CHALLENGE_ID = "test"
INPUT_FILE = os.path.join(
    os.path.realpath(os.path.dirname(__file__)), "dummy_input.txt"
)
COMMENT_SYMBOL = "#"


class DummyChallenge(Challenge):
    @classmethod
    def id(cls):
        return CHALLENGE_ID

    def _solve(self):
        # Example logic:
        with open(INPUT_FILE, "r") as file:
            challenge_input = file.readlines()

        result = ""
        for line in challenge_input:
            if not self._is_comment(line):
                if line.strip() == "":
                    result += " "
                else:
                    result += line[0]

        self.set_solution(solution_part1=result, solution_part2="unused")

    @staticmethod
    def _is_comment(line: str) -> bool:
        return line.startswith(COMMENT_SYMBOL)

    def _print_solution(self):
        print(f"Solution: ")
        print(f"The secret message hidden in the input file is '{self.solution_part1}'")
