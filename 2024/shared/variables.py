from typing import Type

from challenge import Challenge
from dummy_challenge import DummyChallenge

# TODO: update the list below each time a new problem is resolved
#   --> parts 1 and 2 of a day are 2 different problems
ALL_SOLVED_CHALLENGES: list[Type[Challenge]] = [
    DummyChallenge,
]
