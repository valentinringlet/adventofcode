from typing import Type

from shared.challenge import Challenge
from challenges.dummy.dummy_challenge import DummyChallenge
from challenges.day01.challenge_day01 import ChallengeDay01


# TODO: update the list below each time a new problem is resolved
#   --> parts 1 and 2 of a day are 2 different problems
ALL_SOLVED_CHALLENGES: list[Type[Challenge]] = [
    DummyChallenge,
    ChallengeDay01,
]
