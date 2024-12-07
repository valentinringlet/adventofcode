from typing import Type

from shared.challenge import Challenge
from shared.variables import ALL_SOLVED_CHALLENGES


def get_solved_challenges() -> list[Type[Challenge]]:
    return ALL_SOLVED_CHALLENGES


def get_solved_challenges_ids() -> list[str]:
    return [challenge.id() for challenge in get_solved_challenges()]


def print_intro_message():
    print(
        "Hello! The following challenges of the [Advent of Code 2024] have been solved so far:"
    )
    print(get_solved_challenges_ids())
    print("\nWhich challenge would you like to run?")


def print_wrong_input_message():
    print("Plase input one of the ids listed below:")
    print(get_solved_challenges_ids())
    print("\nWhich challenge would you like to run?")


def is_user_input_valid_challenge_id(user_input: str) -> bool:
    valid_challenge_ids = get_solved_challenges_ids()
    valid_challenge_ids_lowercase = [
        challenge_id.lower() for challenge_id in valid_challenge_ids
    ]

    return user_input.lower() in valid_challenge_ids_lowercase


def get_selected_challenge(selected_challenge_id: str) -> Challenge:
    solved_challenges = get_solved_challenges()
    selected_challenge_types = list(
        filter(
            lambda challenge: challenge.id().lower() == selected_challenge_id.lower(),
            solved_challenges,
        )
    )

    if len(selected_challenge_types) != 1:
        raise ValueError("Multiple challenges correspond to the provided id")
    else:
        selected_challenge_type = selected_challenge_types[0]
        return selected_challenge_type()
