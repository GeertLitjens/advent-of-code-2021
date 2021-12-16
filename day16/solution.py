"""
Ah, yes, welcome to recursive function hell. I tend to hate these assignments because they are such a pain to debug.
Today I compounded the issue by getting into a type overflow issues because I combined numpy mathematical operators with
Python types. Note to self: do all numpy or all base Python. In the end it worked out, it is very similar to parsing
headers of binary files and I have ample experience with that now.
"""

from utils import Solution
from typing import Any
import numpy as np


class DaySolution(Solution):
    def __init__(self, day: int = 16, year: int = 2021) -> None:
        super().__init__(day, year)

    def _parse_data(self, input_data: str) -> Any:
        """
        The main tricky thing is that Python will get rid of any leading zeros when converting to binary strings, e.g.
        2 in hexidecimal notation will be 10 instead of 0010. As such I convert every character individually and use
        zfill to add back the leading zeros. Of course strip the empty spaces such as newlines first.
        """
        return "".join([bin(int(x, 16))[2:].zfill(4) for x in input_data.strip()])

    def _parse_packet(self, bin_str: str, idx: int, ver_sum: int):
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
            return idx, ver_sum, int(bin_value, 2)
        else:
            expr_values = []
            l_id = bin_str[idx]
            idx += 1
            if l_id == "0":
                length_in_bits = int(bin_str[idx:idx + 15], 2)
                idx += 15
                end_point = idx + length_in_bits
                while idx < end_point:
                    idx, ver_sum, expr_value = self._parse_packet(bin_str, idx, ver_sum)
                    expr_values.append(expr_value)
            else:
                length_in_subpackets = int(bin_str[idx:idx + 11], 2)
                idx += 11
                for _ in range(length_in_subpackets):
                    idx, ver_sum, expr_value = self._parse_packet(bin_str, idx, ver_sum)
                    expr_values.append(expr_value)
            if tp == 0:
                return idx, ver_sum, sum(expr_values)
            elif tp == 1:
                res = 1
                for x in expr_values:
                    res *= x
                return idx, ver_sum, res
            elif tp == 2:
                return idx, ver_sum, min(expr_values)
            elif tp == 3:
                return idx, ver_sum, max(expr_values)
            elif tp == 5:
                return idx, ver_sum, int(expr_values[0] > expr_values[1])
            elif tp == 6:
                return idx, ver_sum, int(expr_values[0] < expr_values[1])
            elif tp == 7:
                return idx, ver_sum, int(expr_values[0] == expr_values[1])

    def _solve_part1(self, parsed_data: Any) -> Any:
        """
        In the end I combined all the logic into a single function that I use for both part 1 and part 2, a recursive
        parse_packet function. It first looks at the type and decides on the literal vs. operator branches. Then the
        tricky part of the exercise is that the operator part has two different behaviors, which need slightly different
        treatment: for the operator using bit length, you need to check whether the index exceeds the length. The
        operator that uses the number of subpackets is a bit simpler, you simply loop over the number.
        """
        return self._parse_packet(parsed_data, 0, 0)[1]

    def _solve_part2(self, parsed_data: Any) -> Any:
        """
        The main logic was in port 1, but still part 2 took me most time due to some stupid integer overflow with the
        numpy operators. After I switched to pure Python it worked out. The main addition is a simple list of if
        statements. Probably this could have been done nice with a dictionary and a map, but I didn't feel like working
        on it anymore :).
        """
        return self._parse_packet(parsed_data, 0, 0)[2]
