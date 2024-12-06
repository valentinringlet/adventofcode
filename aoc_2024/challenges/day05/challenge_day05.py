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
        input_file = "input_day05.txt"
        input_file_path = os.path.join(os.path.dirname(__file__), input_file)
        input_data = self.parse_input(input_file_path)

        # 2. solve challenge using input data
        solution_part1 = self._solve_part1(input_data)
        solution_part2 = self._solve_part2(input_data)

        # 3. set solution
        self.set_solution(DaySolutionDTO(str(solution_part1), str(solution_part2)))

    def _print_solution(self):
        solution = self.get_solution()
        print(
            f"- part 1: The sum of the middle pages of valid page updates is {solution.solution_part1}"
        )
        print(
            f"- part 2: The sum of the middle pages of the invalid page updates (after reordering to make them valid) is {solution.solution_part2}"
        )

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

    def _solve_part2(
        self, input_data: tuple[list[tuple[int, int]], list[list[int]]]
    ) -> int:
        page_ordering_rules, page_updates = input_data
        invalid_updates = self._get_invalid_updates(page_ordering_rules, page_updates)
        reordered_invalid_updates = [
            self._reorder_update_to_make_valid(page_ordering_rules, page_update)
            for page_update in invalid_updates
        ]
        sum_middle_pages = sum(
            [update[len(update) // 2] for update in reordered_invalid_updates]
        )
        return sum_middle_pages

    def _get_invalid_updates(
        self,
        page_ordering_rules: list[tuple[int, int]],
        page_updates: list[list[int]],
    ):
        valid_updates = self._get_valid_updates(page_ordering_rules, page_updates)
        invalid_updates = [
            update for update in page_updates if update not in valid_updates
        ]
        return invalid_updates

    def _reorder_update_to_make_valid(
        self,
        page_ordering_rules: list[tuple[int, int]],
        update_to_reorder: list[int],
    ) -> list[int]:
        page_ordering_rules_dict = self._make_dict_of_ordering_rules(
            page_ordering_rules,
            key_selector=page_that_should_come_after_selector,
            value_selector=page_that_should_come_before_selector,
        )

        relevant_page_ordering_rules = defaultdict(list)
        for page in update_to_reorder:
            pages_that_should_come_before_it = page_ordering_rules_dict[page]
            pages_from_update_to_reorder = [
                p for p in pages_that_should_come_before_it if p in update_to_reorder
            ]
            relevant_page_ordering_rules[page] = pages_from_update_to_reorder

        reordered_update = []
        # Add the pages in order from the one with the least constraints to the one with most constraints
        pages_to_reorder = sorted(
            update_to_reorder, key=lambda page: len(relevant_page_ordering_rules[page])
        )
        for page in pages_to_reorder:
            # Find the highest index at which there is a page that should appear before `page`
            pages_that_should_appear_before = relevant_page_ordering_rules[page]
            max_idx_page_to_appear_before = 0
            for page_to_appear_before in pages_that_should_appear_before:
                try:
                    idx = reordered_update.index(page_to_appear_before)
                    max_idx_page_to_appear_before = max(
                        idx, max_idx_page_to_appear_before
                    )
                except ValueError:
                    pass  # the page does not appear in reordered update

            # Insert the new page right after the last page it should appear after
            reordered_update.insert(max_idx_page_to_appear_before + 1, page)

        return reordered_update
