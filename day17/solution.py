"""
"""

from utils import Solution
from typing import Any
import math


class DaySolution(Solution):
    def __init__(self, day: int = 17, year: int = 2021) -> None:
        super().__init__(day, year)

    def _parse_data(self, input_data: str) -> Any:
        """
        """
        xmin, xmax = [int(x) for x in input_data.split("target area: x=")[1].split(", y")[0].split("..")]
        ymin, ymax = [int(x) for x in input_data.split(", y=")[1].split("..")]
        return [xmin, xmax, ymin, ymax]

    def _solve_part1(self, parsed_data: Any) -> Any:
        """
        """
        return abs(parsed_data[2]) * (abs(parsed_data[2]) - 1) / 2

    def _solve_part2(self, parsed_data: Any) -> Any:
        """
        """
        xmin, xmax, ymin, ymax = parsed_data
        vymax = ymin
        vymin = -ymin
        vxmax = xmax
        vxmin = math.ceil((math.sqrt(1 + 8 * xmin) - 1) / 2)
        hits = 0
        for cur_vx in range(vxmin, vxmax + 1):
            for cur_vy in range(vymax, vymin + 1):
                vy = cur_vy
                vx = cur_vx
                pos_x = 0
                pos_y = 0
                while True:
                    pos_x += vx
                    pos_y += vy
                    if vx != 0:
                        vx = vx - 1
                    vy -= 1
                    if pos_x > xmax or pos_y < ymin:
                        break
                    elif xmin <= pos_x <= xmax and ymin <= pos_y <= ymax:
                        hits += 1
                        break
        return hits
