"""
"""

from utils import Solution
from typing import Any
from math import ceil


class DaySolution(Solution):
    def __init__(self, day: int = 18, year: int = 2021) -> None:
        super().__init__(day, year)

    def _parse_data(self, input_data: str) -> Any:
        """
        """
        return [[int(x) if x.isdigit() else x for x in line] for line in input_data.strip().split("\n")]

    def _add(self, snf_nr_1, snf_nr_2):
        return ["["] + snf_nr_1 + [","] + snf_nr_2 + ["]"]

    def _perform_actions(self, snf_nr):
        changed = True
        while changed:
            changed = False
            depth = 0
            for i, c in enumerate(snf_nr):
                if c == "[":
                    depth += 1
                elif c == "]":
                    depth -= 1
                if depth > 4:
                    snf_nr = self._explode(snf_nr, i)
                    changed = True
                    break
            for i, c in enumerate(snf_nr):
                if changed:
                    break
                if isinstance(c, int):
                    if int(c) > 9:
                        snf_nr = self._split(snf_nr, i)
                        changed = True
                        break
        return snf_nr

    def _explode(self, snf_nr, i):
        left_int = snf_nr[i+1]
        right_int = snf_nr[i+3]
        for j in range(i, -1, -1):
            if isinstance(snf_nr[j], int):
                snf_nr[j] += left_int
                break
        for j in range(i + 4, len(snf_nr)):
            if isinstance(snf_nr[j], int):
                snf_nr[j] += right_int
                break
        snf_nr[i:i+5] = [0]
        return snf_nr

    def _split(self, snf_nr, i):
        snf_nr[i:i + 1] = ["["] + [snf_nr[i] // 2] + [","] + [ceil(snf_nr[i] / 2)] + ["]"]
        return snf_nr

    def _magnitude(self, snf_nr):
        while len(snf_nr) != 1:
            for i, c in enumerate(snf_nr):
                if isinstance(c, int):
                    if isinstance(snf_nr[i+2], int):
                        snf_nr[i - 1:i + 4] = [3 * c + 2 * snf_nr[i+2]]
                        break
        return snf_nr[0]

    def _solve_part1(self, parsed_data: Any) -> Any:
        """
        """
        start_nr = parsed_data[0]
        for nr in parsed_data[1:]:
            start_nr = self._add(start_nr, nr)
            start_nr = self._perform_actions(start_nr)
        return self._magnitude(start_nr)

    def _solve_part2(self, parsed_data: Any) -> Any:
        """
        """
        max_mag = 0
        for nr_1 in parsed_data:
            for nr_2 in parsed_data:
                start_nr = self._add(nr_1, nr_2)
                start_nr = self._perform_actions(start_nr)
                cur_mag = self._magnitude(start_nr)
                if cur_mag > max_mag:
                    max_mag = cur_mag
        return max_mag
