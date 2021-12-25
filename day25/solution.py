"""
"""

from utils import Solution
from typing import Any
import numpy as np


class DaySolution(Solution):
    def __init__(self, day: int = 25, year: int = 2021) -> None:
        super().__init__(day, year)

    def _parse_data(self, input_data: str) -> Any:
        """
        """
        c_to_int = {'.': 0, '>': 1, 'v': 2}
        seac_map = np.array([[c_to_int[x] for x in line] for line in input_data.strip().split("\n")])
        return seac_map

    def _solve_part1(self, parsed_data: Any) -> Any:
        """
        """
        nr_turns = 0
        cur_map = parsed_data.copy()
        map_shape = cur_map.shape
        while True:
            new_map = cur_map.copy()
            nr_turns += 1
            e_c_row, e_c_col = np.where(cur_map == 1)
            to_move = []
            for p in zip(e_c_row, e_c_col):
                to_col = (p[1] + 1) % map_shape[1]
                if cur_map[p[0], to_col] == 0:
                    to_move.append([p, to_col])
            for m_p in to_move:
                new_map[m_p[0][0], m_p[1]] = 1
                new_map[m_p[0][0], m_p[0][1]] = 0
            s_c_row, s_c_col = np.where(cur_map == 2)
            to_move = []
            for p in zip(s_c_row, s_c_col):
                to_row = (p[0] + 1) % map_shape[0]
                if new_map[to_row, p[1]] == 0:
                    to_move.append([p, to_row])
            for m_p in to_move:
                new_map[m_p[1], m_p[0][1]] = 2
                new_map[m_p[0][0], m_p[0][1]] = 0
            if (new_map == cur_map).all():
                break
            else:
                cur_map = new_map
        return nr_turns

    def _solve_part2(self, parsed_data: Any) -> Any:
        """
        """
        return 1
