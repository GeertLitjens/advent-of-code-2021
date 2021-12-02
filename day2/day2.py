from utils import Solution
from typing import Any


class DaySolution(Solution):
    def __init__(self, day: int = 2, year: int = 2021) -> None:
        super().__init__(day, year)

    def _parse_data(self, input_data: str) -> Any:
        return [x.split(" ") for x in input_data.split("\n") if x]

    def _solve_part1(self, parsed_data: Any) -> Any:
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
