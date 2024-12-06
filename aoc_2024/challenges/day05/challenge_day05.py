import os
from collections import defaultdict
from collections.abc import Callable

from shared.challenge import Challenge, DaySolutionDTO


def page_that_should_come_before_selector(page_ordering_rule: tuple[int, int]) -> int:
    return page_ordering_rule[0]


def page_that_should_come_after_selector(page_ordering_rule: tuple[int, int]) -> int:
    return page_ordering_rule[1]


class ChallengeDay05(Challenge):
    @classmethod
    def id(cls) -> str:
        return "Day5"

    def _solve(self):
        # 1. read input data
        input_file = "input_day05.txt"  # "test_input_part1.txt"
        input_file_path = os.path.join(os.path.dirname(__file__), input_file)
        input_data = self.parse_input(input_file_path)

        # 2. solve challenge using input data
        solution_part1 = self._solve_part1(input_data)
        # TODO part 2

        # 3. set solution
        self.set_solution(DaySolutionDTO(str(solution_part1), "not solved yet"))

    def _print_solution(self):
        solution = self.get_solution()
        # TODO: write what the answer represents
        print(
            f"- part 1: The sum of the middle pages of valid page updates is {solution.solution_part1}"
        )
        print(f"- part 2: {solution.solution_part2}")

    @staticmethod
    def parse_input(file_path: str) -> tuple[list[tuple[int, int]], list[list[int]]]:
        with open(file_path, "r") as file:
            page_ordering_rules = []
            next_line = file.readline()
            while next_line.strip() != "":
                page_before, page_after = next_line.strip().split("|")
                page_ordering_rules.append((int(page_before), int(page_after)))
                next_line = file.readline()

            page_updates = []
            next_line = file.readline()
            while next_line.strip() != "":
                pages_in_update = next_line.strip().split(",")
                pages_in_update = [int(page.strip()) for page in pages_in_update]
                page_updates.append(pages_in_update)
                next_line = file.readline()

            return page_ordering_rules, page_updates

    def _solve_part1(
        self, input_data: tuple[list[tuple[int, int]], list[list[int]]]
    ) -> int:
        page_ordering_rules, page_updates = input_data
        valid_updates = self._get_valid_updates(page_ordering_rules, page_updates)
        sum_middle_pages = sum([update[len(update) // 2] for update in valid_updates])
        return sum_middle_pages

    def _get_valid_updates(
        self,
        page_ordering_rules: list[tuple[int, int]],
        page_updates: list[list[int]],
    ):
        page_ordering_rules_dict = self._make_dict_of_ordering_rules(
            page_ordering_rules,
            key_selector=page_that_should_come_before_selector,
            value_selector=page_that_should_come_after_selector,
        )

        valid_page_updates = []
        for update in page_updates:
            pages_seen_in_curr_update = []
            valid_update = True
            for curr_page in update:
                pages_to_appear_after_curr_page = page_ordering_rules_dict[curr_page]
                pages_seen_before_that_should_appear_after = set(
                    pages_seen_in_curr_update
                ).intersection(pages_to_appear_after_curr_page)
                if len(pages_seen_before_that_should_appear_after) != 0:
                    valid_update = False
                    break

                pages_seen_in_curr_update.append(curr_page)

            if valid_update:
                valid_page_updates.append(update)

        return valid_page_updates

    @staticmethod
    def _make_dict_of_ordering_rules(
        page_ordering_rules: list[tuple[int, int]],
        key_selector: Callable[[tuple[int, int]], int],
        value_selector: Callable[[tuple[int, int]], int],
    ) -> dict[int, list[int]]:
        ordering_rules_dict = defaultdict(list)
        for rule in page_ordering_rules:
            key = key_selector(rule)
            value = value_selector(rule)
            ordering_rules_dict[key].append(value)
        return ordering_rules_dict
