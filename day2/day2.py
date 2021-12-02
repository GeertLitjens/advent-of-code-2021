"""
Day 2 was also relatively straightforward, not much challenge up till now. The only stumbling block was that I first
did not read that the up and down in part 2 no longer changed the depth by themselves. Other than that, smooth sailing.
"""

from utils import Solution
from typing import Any


class DaySolution(Solution):
    def __init__(self, day: int = 2, year: int = 2021) -> None:
        super().__init__(day, year)

    def _parse_data(self, input_data: str) -> Any:
        """
        The input consists of two parts, so let's split on the newline and then on the space two have every
        instruction separate and to be able to separate the direction and magnitude.
        """
        return [x.split(" ") for x in input_data.split("\n") if x]

    def _solve_part1(self, parsed_data: Any) -> Any:
        """
        First identify the direction and then add or subtract the magnitude from the corresponding position.
        Don't forget that the magnitude still needs to be converted to int.
        """
        x = 0
        d = 0
        for direction in parsed_data:
            if direction[0] == "forward":
                x += int(direction[1])
            elif direction[0] == "up":
                d -= int(direction[1])
            else:
                d += int(direction[1])
        return x * d

    def _solve_part2(self, parsed_data: Any) -> Any:
        """
        This took one more attempt because I didn't read carefully and kept the depth addition/substraction for the
        up and down direction in the code first. Easy fix afterwards.
        """
        x = 0
        d = 0
        aim = 0
        for direction in parsed_data:
            if direction[0] == "forward":
                x += int(direction[1])
                d += aim * int(direction[1])
            elif direction[0] == "up":
                aim -= int(direction[1])
            else:
                aim += int(direction[1])
        return x * d
