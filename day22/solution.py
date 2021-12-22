"""
"""

from utils import Solution
from typing import Any
import numpy as np


class DaySolution(Solution):
    def __init__(self, day: int = 22, year: int = 2021) -> None:
        super().__init__(day, year)

    def _parse_data(self, input_data: str) -> Any:
        """
        """
        lines = input_data.strip().split("\n")
        instructions = []
        for line in lines:
            instructions.append({"value": 1 if line.split(" ")[0] == "on" else 0,
                                 "x": [int(x) for x in line.split("x=")[1].split(",")[0].split("..")],
                                 "y": [int(x) for x in line.split("y=")[1].split(",")[0].split("..")],
                                 "z": [int(x) for x in line.split("z=")[1].split(",")[0].split("..")]})
        return instructions

    def _solve_part1(self, parsed_data: Any) -> Any:
        """
        """
        space = np.zeros((101, 101, 101), dtype="ubyte")
        for ins in parsed_data:
            space[ins["z"][0] + 50:ins["z"][1] + 50 + 1,
                  ins["y"][0] + 50:ins["y"][1] + 50 + 1,
                  ins["x"][0] + 50:ins["x"][1] + 50 + 1] = ins["value"]
        return space.sum()

    def _solve_part2(self, parsed_data: Any) -> Any:
        """
        """
        return 1
