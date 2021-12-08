"""
Quite a challenging puzzle today, at least part 2. Part 1 was mostly complicated due to the large amount of story text,
which you really did not need to solve that part. Other than that, I over-engineered part 2 initially by figuring out
exactly which segment corresponded to which letter in the code, but that seemed to be completely unnecessary after I
finished the assignment because I realized you can identify any number by just using set intersection with the numbers
you know because of their length. For example, 2 is the only number with 5 segments and 2 overlapping segments with 4,
which you can identify uniquely because it has 4 segments. After this I simplified the code to what it is now. As such,
mostly a conceptual exercise, but the programming part was straightforward.
"""

from utils import Solution
from typing import Any
import numpy as np


class DaySolution(Solution):
    def __init__(self, day: int = 8, year: int = 2021) -> None:
        super().__init__(day, year)

    def _parse_data(self, input_data: str) -> Any:
        """
        Data parsing is pretty straightforward. First split the lines, then the patterns and output values on the |
        separator. Finally, we create sets for the individual patterns and output sections to allow set operations later
        on.
        """
        lines = [x for x in input_data.split("\n") if x]
        patterns = [line.split(" | ")[0] for line in lines]
        output_values = [line.split(" | ")[1] for line in lines]
        patterns = [[set(y) for y in x.split(" ")] for x in patterns]
        output_values = [[set(y) for y in x.split(" ")] for x in output_values]
        return patterns, output_values

    def _solve_part1(self, parsed_data: Any) -> Any:
        """
        Part 1 has a very simple solution, you just calculate the length of the output values and if it is either 2, 3,
        4 or 7 it is one of the simple numbers. Just count them and return, we can even do it in a 1-line list
        comprehension.
        """
        patterns, output_values = parsed_data
        return np.sum([1 for output_value in output_values for value in output_value if len(value) in [2, 3, 4, 7]])

    def _solve_part2(self, parsed_data: Any) -> Any:
        """
        Part 2 was trickier and mostly required a bit of logical reasoning. The key here is that any number can be
        expressed by the number of segments and the overlapping segments with other numbers. For example, 1, 4, 7 and 8
        are identifiable by their number of segments alone because they are unique. However, there are 3 numbers with
        5 segments (2, 3, and 5) and 3 numbers with 6 segments (6, 9 and 0). These can be identified by looking at the
        overlap between them and 1, 4, 7, 8. For example, 3 is the only 5-segment number with 3 overlapping segments
        with 7. As such, if there are three letters in common between a 5-segment number and 7, it has to be 3. You can
        make a rule for each number and the simply check the output values against it. Then you finish the puzzle by
        simply adding up the resultant integers.
        """
        solution = 0
        patterns, output_values = parsed_data
        for pattern, output_value in zip(patterns, output_values):
            # First get 1, 4, 7 and 8
            len_to_pattern = {len(x): x for x in pattern}
            one = len_to_pattern[2]
            four = len_to_pattern[4]
            seven = len_to_pattern[3]

            out_string = ""
            for val in output_value:
                val_len = len(val)
                if val_len == 2:
                    out_string += "1"
                elif val_len == 3:
                    out_string += "7"
                elif val_len == 4:
                    out_string += "4"
                elif val_len == 7:
                    out_string += "8"
                elif val_len == 5 and len(val & four) == 2:
                    out_string += "2"
                elif val_len == 5 and len(val & seven) == 3:
                    out_string += "3"
                elif val_len == 5 and len(val & four) == 3 and len(val & one) == 1:
                    out_string += "5"
                elif val_len == 6 and len(val & four) == 4:
                    out_string += "9"
                elif val_len == 6 and len(val & four) == 3 and len(val & one) == 1:
                    out_string += "6"
                elif val_len == 6 and len(val & four) == 3 and len(val & one) == 2:
                    out_string += "0"
            solution += int(out_string)
        return solution
