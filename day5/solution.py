"""
I think the key challenge today was to really subdivide the problem into two parts. First, put most of the logic related
to the orientation and coordinates of the line in a separate class. Then in the problem itself we focus on keeping track
of the hit rate of the different coordinates. In that way the logical statements (i.e. is equal, greater than, etc.)
can be simpler.
"""

from utils import Solution
from typing import Any
from collections import defaultdict
import numpy as np


class Line:
    """
    This class contains all the logic for getting line coordinates. Note that it only works under the assumption that
    lines are either horizontal, vertical or have a 45-degree angle. In the init function we determine the
    directionality in the x and y directions using the sign function. In traverse we simply iterate from the start to
    the end of the line using a generator function.
    """
    def __init__(self, point_1: tuple[int, int], point_2: tuple[int, int]) -> None:
        self._x0, self._y0 = point_1
        self._x1, self._y1 = point_2
        self._dir_x = np.sign(self._x1 - self._x0)
        self._dir_y = np.sign(self._y1 - self._y0)

    def is_horizontal(self) -> bool:
        return self._y0 == self._y1

    def is_vertical(self) -> bool:
        return self._x0 == self._x1

    def traverse(self) -> tuple[int, int]:
        cur_x = self._x0
        cur_y = self._y0
        while cur_x != self._x1 + self._dir_x or cur_y != self._y1 + self._dir_y:
            yield cur_x, cur_y
            cur_x += self._dir_x
            cur_y += self._dir_y


class DaySolution(Solution):
    def __init__(self, day: int = 5, year: int = 2021) -> None:
        super().__init__(day, year)

    def _parse_data(self, input_data: str) -> Any:
        """
        Pretty straightforward parsing again, simply split the lines to obtain the different line definitions. Then
        split on the arrow character to get the begin and end points. These points are then converted to int's and fed
        to the initialization function of the line class.
        """
        lines_string = [x for x in input_data.split("\n") if x]
        lines = []
        for line in lines_string:
            coord1, coord2 = line.split(" -> ")
            x0, y0 = [int(x) for x in coord1.split(",")]
            x1, y1 = [int(x) for x in coord2.split(",")]
            lines.append(Line((x0, y0), (x1, y1)))
        return lines

    def _discover_danger_points(self, parsed_data: list[Line], check_straight: bool = True):
        """
        Simply check the count a coordinate is hit using a dictionary object. This is more memory efficient than a list
        or array because we have sparse points along broad dimensions. We check here whether we should only should
        consider straight lines and whether the line is actually horizontal and vertical.
        """
        coord_checker = defaultdict(int)
        for line in parsed_data:
            if not check_straight or (line.is_horizontal() or line.is_vertical()):
                for coord in line.traverse():
                    coord_checker[coord] += 1
        danger_points = np.array(list(coord_checker.values()))
        return (danger_points > 1).sum()

    def _solve_part1(self, parsed_data: list[Line]) -> Any:
        """
        This was the first time this year that I created a separate class to handle most of the logic of the problem.
        That simplifies this function significantly. As the only difference between part 1 and 2 is whether diagonal
        lines should be considered I implemented a separate parameterized function to handle this.
        """
        return self._discover_danger_points(parsed_data)

    def _solve_part2(self, parsed_data: list[Line]) -> Any:
        """
        Exactly the same implementation as part 1, just one different parameter to make sure we consider diagonal lines.
        """
        return self._discover_danger_points(parsed_data, False)
