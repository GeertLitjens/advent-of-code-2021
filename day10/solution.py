"""
"""

from utils import Solution
from typing import Any
import numpy as np


class DaySolution(Solution):
    def __init__(self, day: int = 10, year: int = 2021) -> None:
        super().__init__(day, year)
        self._open_to_close = {"(": ")", "[": "]", "{":"}", "<": ">"}
        self._char_to_cost = {")": 3, "]": 57, "}": 1197, ">": 25137}
        self._char_to_points = {")": 1, "]": 2, "}": 3, ">": 4}

    def _parse_data(self, input_data: str) -> Any:
        """
        """
        return [x for x in input_data.split("\n") if x]

    def _check_line(self, line):
        stack = []
        for char in line:
            if char in self._open_to_close.keys():
                stack.append(self._open_to_close[char])
            elif char in self._open_to_close.values():
                close_char = stack.pop()
                if close_char != char:
                    return True, char, stack
        return False, "", stack

    def _solve_part1(self, parsed_data: Any) -> Any:
        """
        """
        cost = 0
        for line in parsed_data:
            invalid, wrong_char, stack = self._check_line(line)
            if invalid:
                cost += self._char_to_cost[wrong_char]
        return cost

    def _solve_part2(self, parsed_data: Any) -> Any:
        """
        """
        points = []
        for line in parsed_data:
            invalid, wrong_char, stack = self._check_line(line)
            if not invalid:
                points_for_line = 0
                for close_char in reversed(stack):
                    points_for_line = points_for_line * 5 + self._char_to_points[close_char]
                points.append(int(points_for_line))
        return np.median(points)
