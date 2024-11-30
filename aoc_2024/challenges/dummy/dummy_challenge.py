from shared.challenge import Challenge


CHALLENGE_ID = "test"


class DummyChallenge(Challenge):
    @classmethod
    def id(cls):
        return CHALLENGE_ID

    def __init__(self):
        super().__init__()

    def solve(self):
        print("Some logic will be executed here.")
        print("Good job reaching this!")
