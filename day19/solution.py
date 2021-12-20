"""
"""

from utils import Solution
from typing import Any
import numpy as np


class DaySolution(Solution):
    def __init__(self, day: int = 19, year: int = 2021) -> None:
        super().__init__(day, year)

    def _parse_data(self, input_data: str) -> Any:
        """
        """
        scanners = []
        scanners_unparsed = input_data.strip().split("\n\n")
        for i, scanner in enumerate(scanners_unparsed):
            coords = [[int(x) for x in coord.split(",")] for coord in scanner.split("\n")[1:]]
            scanners.append({"coords": coords})
        return scanners

    def _solve_part1(self, parsed_data: Any) -> Any:
        """
        """
        # Calculate distances
        for scanner in parsed_data:
            coords = scanner["coords"]
            distances = []
            for c_1 in coords:
                coord_distances = []
                for c_2 in coords:
                    if c_1 == c_2:
                        continue
                    coord_distances.append(np.abs(c_1[0] - c_2[0]) + np.abs(c_1[1] - c_2[1]) + np.abs(c_1[2] - c_2[2]))
                distances.append(coord_distances)
            scanner['distances'] = distances

        # Determine overlapping scanners
        for i, s_1 in enumerate(parsed_data):
            d_1 = s_1["distances"]
            for j, s_2 in enumerate(parsed_data):
                if i != j:
                    d_2 = s_2["distances"]
        return 1

    def _solve_part2(self, parsed_data: Any) -> Any:
        """
        """
        return 1
