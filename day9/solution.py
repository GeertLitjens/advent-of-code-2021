"""
"""

from utils import Solution
from typing import Any
import numpy as np
from skimage.segmentation import watershed
from skimage.measure import regionprops
from skimage.feature import peak_local_max


class DaySolution(Solution):
    def __init__(self, day: int = 9, year: int = 2021) -> None:
        super().__init__(day, year)

    def _parse_data(self, input_data: str) -> Any:
        """
        """
        return np.array([[int(char) for char in x] for x in input_data.split("\n") if x])

    def _solve_part1(self, parsed_data: Any) -> Any:
        """
        """
        padded_data = np.pad(parsed_data, ((1, 1), (1, 1)), 'constant', constant_values=9)
        min_coords = peak_local_max(-padded_data)
        return np.sum(padded_data[tuple(min_coords.T)] + 1)

    def _solve_part2(self, parsed_data: Any) -> Any:
        """
        """
        labels = watershed(parsed_data, mask=parsed_data != 9)
        props = regionprops(labels)
        return np.prod(sorted([prop.area for prop in props])[-3:])
