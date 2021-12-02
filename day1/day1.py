from utils import Solution
from typing import Any


class DaySolution(Solution):

    def _parse_data(self, input_data: str) -> Any:
        return [int(x) for x in input_data.split("\n") if x]

    def _solve_part1(self, parsed_data: Any) -> Any:
        count_diff = 0
        prev_val = parsed_data[0]
        for i in range(1, len(parsed_data)):
            cur_val = parsed_data[i]
            if cur_val > prev_val:
                count_diff += 1
            prev_val = cur_val
        return count_diff

    def _solve_part2(self, parsed_data: Any) -> Any:
        count_diff = 0
        prev_val = sum(parsed_data[0:3])
        for i in range(1, len(parsed_data) - 2):
            cur_val = sum(parsed_data[i:i+3])
            if cur_val > prev_val:
                count_diff += 1
            prev_val = cur_val
        return count_diff
