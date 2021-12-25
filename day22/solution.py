"""
"""

from utils import Solution
from typing import Any
import numpy as np
from collections import Counter


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
        cubes = Counter()
        for ins in parsed_data:
            update = Counter()
            nsgn = ins["value"] or -1
            nx0, nx1 = ins["x"]
            ny0, ny1 = ins["y"]
            nz0, nz1 = ins["z"]
            for (ex0, ex1, ey0, ey1, ez0, ez1), esgn in cubes.items():
                ix0 = max(nx0, ex0)
                ix1 = min(nx1, ex1)
                iy0 = max(ny0, ey0)
                iy1 = min(ny1, ey1)
                iz0 = max(nz0, ez0)
                iz1 = min(nz1, ez1)
                if ix0 <= ix1 and iy0 <= iy1 and iz0 <= iz1:
                    update[(ix0, ix1, iy0, iy1, iz0, iz1)] -= esgn
            if nsgn > 0:
                update[(nx0, nx1, ny0, ny1, nz0, nz1)] += nsgn
            cubes.update(update)

        return sum((x1 - x0 + 1) * (y1 - y0 + 1) * (z1 - z0 + 1) * sgn
                   for (x0, x1, y0, y1, z0, z1), sgn in cubes.items())