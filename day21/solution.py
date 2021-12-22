"""
"""

from utils import Solution
from typing import Any
from functools import cache


class DaySolution(Solution):
    def __init__(self, day: int = 21, year: int = 2021) -> None:
        super().__init__(day, year)

    def _parse_data(self, input_data: str) -> Any:
        """
        """
        p1, p2 = [int(x[-1]) for x in input_data.strip().split("\n")]
        return p1, p2

    def _solve_part1(self, parsed_data: Any) -> Any:
        """
        """
        p1, p2 = parsed_data
        p1_s, p2_s = 0, 0
        dies_rolled = 0
        while True:
            dies_rolled += 3
            p1_forward = (dies_rolled * (dies_rolled + 1) / 2) - ((dies_rolled - 3) * (dies_rolled - 2) / 2)
            p1 = (p1 + p1_forward) % 10
            p1_s += p1 if p1 != 0 else 10
            if p1_s > 999:
                break
            dies_rolled += 3
            p2_forward = (dies_rolled * (dies_rolled + 1) / 2) - ((dies_rolled - 3) * (dies_rolled - 2) / 2)
            p2 = (p2 + p2_forward) % 10
            p2_s += p2 if p2 != 0 else 10
            if p2_s > 999:
                break
        return min(p1_s, p2_s) * dies_rolled

    def _solve_part2(self, parsed_data: Any) -> Any:
        """
        """
        p1, p2 = parsed_data

        @cache
        def play_turn(p1, p2, p1_s=0, p2_s=0):
            if p2_s >= 21:
                return 0, 1

            p_w1, p_w2 = 0, 0
            for p_f, n in [(3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1)]:
                p1_ = (p1 + p_f) % 10 or 10
                w2, w1 = play_turn(p2, p1_, p2_s, p1_s + p1_)
                p_w1, p_w2 = p_w1 + n * w1, p_w2 + n * w2
            return p_w1, p_w2

        return max(play_turn(p1, p2))