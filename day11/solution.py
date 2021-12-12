"""
A bit easier than yesterday, I simply solved the puzzle by using np.where in a loop
"""

from utils import Solution
from typing import Any
import numpy as np


class DaySolution(Solution):
    def __init__(self, day: int = 11, year: int = 2021) -> None:
        super().__init__(day, year)

    def _parse_data(self, input_data: str) -> Any:
        """
        """
        return np.array([[int(x) for x in line] for line in input_data.split("\n") if line])

    def _observe_octopi(self, initial_state: np.ndarray, total_steps: int = 0):
        octopi = initial_state.copy()
        total_flashes = 0
        step = 0
        while True:
            octopi += 1
            charged_octopi = np.where(octopi > 9)
            octopi_mask = np.zeros((10, 10))
            while charged_octopi[0].size > 0:
                for row, col in zip(*charged_octopi):
                    if octopi_mask[row, col] == 1:
                        continue
                    octopi_mask[row, col] = 1
                    min_row = row - 1 if row > 0 else row
                    max_row = row + 2 if row < 9 else row + 1
                    min_col = col - 1 if col > 0 else col
                    max_col = col + 2 if col < 9 else col + 1
                    octopi[min_row:max_row, min_col: max_col] += 1
                charged_octopi = np.where(np.logical_and(octopi > 9,  octopi_mask == 0))
            for row, col in zip(*np.where(octopi_mask == 1)):
                octopi[row, col] = 0
            total_flashes += np.sum(octopi_mask)
            if np.sum(octopi_mask) == 100 or step + 1 == total_steps:
                return total_flashes, step + 1
            step += 1

    def _solve_part1(self, parsed_data: np.ndarray) -> Any:
        """
        """
        return self._observe_octopi(parsed_data, 100)[0]

    def _solve_part2(self, parsed_data: np.ndarray) -> Any:
        """
        """
        return self._observe_octopi(parsed_data)[1]

