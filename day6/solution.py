"""
This was a day where I had a lot of benefit from my participation last year. The exponential growth aspect of the
problem immediately signalled to me that I should not try to keep track of individual fish to iterate over, as this
would get prohibitively slow. I quickly realized that I just needed to keep track of how many fish were at each stage,
resulting in only needing to keep track of 9 values (0 - 8). I again used Numpy to get a fast and efficient solution.
"""

from utils import Solution
from typing import Any
import numpy as np


class DaySolution(Solution):
    def __init__(self, day: int = 6, year: int = 2021) -> None:
        super().__init__(day, year)

    def _parse_data(self, input_data: str) -> Any:
        """
        The string parsing part was really straightforward, the fish were indicated in a comma-separated string that I
        convert to a list of int. Subsequently, because I do not need to keep track of the individual fish, but just of
        the number of fish in each stage I calculate a histogram. Each bin contains the amount of fish for that day.
        """
        fishtogram = np.histogram([int(x) for x in input_data.split(",")], bins=9, range=(0, 9))[0]
        return fishtogram

    def _solve_part1(self, parsed_data: np.ndarray) -> Any:
        """
        Once you have the histogram, the solution itself is quite simple. The fish move one stage for each day, which
        is achieved by using the `np.roll` function, which shifts each entry and wraps around. This also make sure the
        newborn fish are added to the end. The only extra step is to also 'reset' the fish that gave birth and add them
        to the reset point (stage 6).
        """
        fishies = parsed_data.copy()
        for day in range(80):
            fishies = np.roll(fishies, -1)
            fishies[6] += fishies[-1]
        return np.sum(fishies)

    def _solve_part2(self, parsed_data: np.ndarray) -> Any:
        """
        Exactly the same as the solution for part 1, just need to increase the number of days.
        """
        fishies = parsed_data.copy()
        for day in range(256):
            fishies = np.roll(fishies, -1)
            fishies[6] += fishies[-1]
        return np.sum(fishies)