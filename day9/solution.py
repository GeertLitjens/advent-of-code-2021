"""
Today was a nice image analysis challenge that I was very familiar with. The only caveat is that using scikit-image does
feel a bit like cheating, but it didn't make sense to me to reimplement a local minima filter and a watershed transform
while perfectly fine and fast version exist within the Python ecosystem. So very simple a short solutions today.
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
        Data parsing was straightforward, simply split the lines and conver the characters to ints.
        """
        return np.array([[int(char) for char in x] for x in input_data.split("\n") if x])

    def _solve_part1(self, parsed_data: Any) -> Any:
        """
        The only thing that required some thought was the border handling. The default options for peak_local_max don't
        work for this specific problem, so I simply padded the input with the highest value, 9. Then I invert the array
        to be able to look for maxima instead of minima. The last part is a simpel sum over the returned coordinates for
        the different minima.
        """
        padded_data = np.pad(parsed_data, ((1, 1), (1, 1)), 'constant', constant_values=9)
        min_coords = peak_local_max(-padded_data)
        return np.sum(padded_data[tuple(min_coords.T)] + 1)

    def _solve_part2(self, parsed_data: Any) -> Any:
        """
        As soon as the text started talking about basins, I knew this was a simple masked watershed transform. I
        directly used the one from scikit-image. Subsequently, I use regionprops to get the area for the individual
        labels, I sort them based on size and get the top 3, which I multiply together.
        """
        labels = watershed(parsed_data, mask=parsed_data != 9)
        props = regionprops(labels)
        return np.prod(sorted([prop.area for prop in props])[-3:])
