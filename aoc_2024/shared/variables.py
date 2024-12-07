from typing import Type

from shared.challenge import Challenge
from challenges.dummy.dummy_challenge import DummyChallenge
from challenges.day01.challenge_day01 import ChallengeDay01
from challenges.day02.challenge_day02 import ChallengeDay02
from challenges.day03.challenge_day03 import ChallengeDay03
from challenges.day04.challenge_day04 import ChallengeDay04
from challenges.day05.challenge_day05 import ChallengeDay05
from challenges.day06.challenge_day06 import ChallengeDay06
from challenges.day07.challenge_day07 import ChallengeDay07


# TODO: update the list below each time a new problem is resolved
#   --> parts 1 and 2 of a day are 2 different problems
ALL_SOLVED_CHALLENGES: list[Type[Challenge]] = [
    DummyChallenge,
    ChallengeDay01,
    ChallengeDay02,
    ChallengeDay03,
    ChallengeDay04,
    ChallengeDay05,
    ChallengeDay06,
    ChallengeDay07,
]
