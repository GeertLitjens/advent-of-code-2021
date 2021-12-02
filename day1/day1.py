"""
My solution for the first day of the new advent of code for 2021. As always, pretty easy and straightforward for this
first day. That has allowed me to spend some more time on creating some nice things around it, such as the webpages
explaining my solutions. Below you can read the story of the first part of the first day.
"""

from utils import Solution
from typing import Any


class DaySolution(Solution):

    def _parse_data(self, input_data: str) -> Any:
        """
        The input data consists of a string of ints, so we split the string on the newline character and then
        convert the individual elements to int.
        """
        return [int(x) for x in input_data.split("\n") if x]

    def _solve_part1(self, parsed_data: Any) -> Any:
        """
        This first task was really straightforward, it was just
        a matter of iterating over the list of items, starting
        from 1 and checking whether the previous value was lower.
        """
        count_diff = 0
        prev_val = parsed_data[0]
        for i in range(1, len(parsed_data)):
            cur_val = parsed_data[i]
            if cur_val > prev_val:
                count_diff += 1
            prev_val = cur_val
        return count_diff

    def _solve_part2(self, parsed_data: Any) -> Any:
        """
        Part 2 was not much more difficult, instead of taking the value itself we now take
        the sum of the next three values while iterating from 1 until length - 2.
        """
        count_diff = 0
        prev_val = sum(parsed_data[0:3])
        for i in range(1, len(parsed_data) - 2):
            cur_val = sum(parsed_data[i:i+3])
            if cur_val > prev_val:
                count_diff += 1
            prev_val = cur_val
        return count_diff
