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

    def __init__(self):
        super().__init__()
        self.__solution = None

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

        self.__solution = result

    @staticmethod
    def _is_comment(line: str) -> bool:
        return line.startswith(COMMENT_SYMBOL)

    def print_solution(self):
        if not self.__solution:
            raise ValueError(
                "Method solve() needs to be called before calling get_solution()"
            )

        print(f"The secret hidden in the input file is '{self.__solution}'")
