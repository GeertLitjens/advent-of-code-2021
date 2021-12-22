"""
"""

from utils import Solution
from typing import Any
import numpy as np
from scipy.ndimage import convolve


class DaySolution(Solution):
    def __init__(self, day: int = 20, year: int = 2021) -> None:
        super().__init__(day, year)
        self._bin2dec = 2 ** np.arange(9).reshape(3, 3)

    def _parse_data(self, input_data: str) -> Any:
        """
        """
        algo, _, *image = input_data.splitlines()

        img_enh = np.array([int(p == "#") for p in algo])
        img = np.pad([[int(p == "#") for p in row]
                      for row in image], (51, 51))

        return img_enh, img

    def _solve_part1(self, parsed_data: Any) -> Any:
        """
        """
        img_enh, img = parsed_data

        for i in range(2):
            img = img_enh[convolve(img, self._bin2dec)]
        return img.sum()

    def _solve_part2(self, parsed_data: Any) -> Any:
        """
        """
        img_enh, img = parsed_data

        for i in range(50):
            img = img_enh[convolve(img, self._bin2dec)]
        return img.sum()
