"""
Today was quite simple again, especially part 1. The key for part 1 was simply the realization that the median position
will always cause the sum of distance to be lowest. Part 2 was a bit more tricky. I did realize that the distance
for part 2 was simply the triangular number, defined as $\frac{n * (n + 1)}\frac{2}$. Then I first simply brute forced
the solution to find the smallest sum of distances, starting at the median. This gave me the correct answer, and then
I spent a bit of time to implement a binary search to optimize the search time.
"""

from utils import Solution
from typing import Any
import numpy as np


class DaySolution(Solution):
    def __init__(self, day: int = 7, year: int = 2021) -> None:
        super().__init__(day, year)

    def _parse_data(self, input_data: str) -> Any:
        """
        Data parsing was again very straightforward, just returning a numpy array of ints.
        """
        return np.array([int(x) for x in input_data.split(",")])

    def _solve_part1(self, parsed_data: Any) -> Any:
        """
        Part 1 was straightforward, the median of a list points will always be the point with the lowest sum of
        distances to the other points in a list.
        """
        return np.sum(np.abs(parsed_data - np.median(parsed_data)))

    def _solve_part2(self, parsed_data: Any) -> Any:
        """
        Part 2 was a bit more tricky. I did know that the given definition of the new distance was a triangular number,
        for example $T_2 = 1 + 2$ and $T_4 = 1 + 2 + 3 + 4$. I couldn't think of a way to solve this analytically, so
        I wrote a simple brute force search, starting from the median point and then going higher. Later I replaced it
        with a binary search to make it more efficient. There might be a better solution, but I'm pretty happy with
        the result.
        """
        low_x = np.median(parsed_data)
        high_x = np.max(parsed_data)
        def calc_min(cur_pos, all_pos): return np.sum([x * (x + 1) / 2 for x in np.abs(all_pos - cur_pos)])
        low_min = calc_min(low_x, parsed_data)
        high_min = calc_min(high_x, parsed_data)
        while low_x != high_x:
            if low_min > high_min:
                low_x = np.ceil((low_x + high_x) / 2)
                low_min = calc_min(low_x, parsed_data)
            else:
                high_x = np.floor((low_x + high_x) / 2)
                high_min = calc_min(high_x, parsed_data)
        return high_min
