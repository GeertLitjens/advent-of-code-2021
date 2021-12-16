"""
"""

from utils import Solution
from typing import Any
import numpy as np


class DaySolution(Solution):
    def __init__(self, day: int = 16, year: int = 2021) -> None:
        super().__init__(day, year)

    def _parse_data(self, input_data: str) -> Any:
        """
        """
        int_val = int(input_data, 16)
        bin_val = bin(int_val)[2:]
        return bin_val.zfill(len(input_data) * 4)

    def _parse_packet(self, bin_str: str, idx: int, end_idx: int, ver_sum: int):
        if ver_sum == 0:
            start = True
        else:
            start = False
        while idx < end_idx:
            ver_sum += int(bin_str[idx:idx + 3], 2)
            tp = int(bin_str[idx + 3:idx + 6], 2)
            idx += 6
            if tp == 4:
                not_last = True
                bin_value = ""
                while not_last:
                    bin_value += bin_str[idx + 1:idx + 5]
                    if bin_str[idx] == "0":
                        not_last = False
                        idx += 5
                    else:
                        idx += 5
                int_value = int(bin_value, 2)
                return idx, ver_sum
            else:
                l_id = bin_str[idx]
                idx += 1
                if l_id == "0":
                    length_in_bits = int(bin_str[idx:idx + 15], 2)
                    idx += 15
                    idx, ver_sum = self._parse_packet(bin_str, idx, idx + length_in_bits, ver_sum)
                else:
                    length_in_subpackets = int(bin_str[idx:idx + 11], 2)
                    idx += 11
                    for _ in range(length_in_subpackets):
                        idx, ver_sum = self._parse_packet(bin_str, idx, end_idx, ver_sum)
            if start:
                break
        return idx, ver_sum


    def _solve_part1(self, parsed_data: Any) -> Any:
        """
        """
        return self._parse_packet(parsed_data, 0, len(parsed_data), 0)[1]

    def _solve_part2(self, parsed_data: Any) -> Any:
        """
        """
        return 1
