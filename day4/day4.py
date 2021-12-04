"""
The puzzles start to become a little more complex. I quickly decided I would again use numpy to solve this puzzle
because it allows efficient summing across different axes. Furthermore, it allows to quickly perform comparisons across
all elements. After solving the first part, the second part was pretty straightforward this time.
"""

from utils import Solution
from typing import Any
import numpy as np


class DaySolution(Solution):
    def __init__(self, day: int = 4, year: int = 2021) -> None:
        super().__init__(day, year)

    def _parse_data(self, input_data: str) -> Any:
        """
        The data parsing was again slightly more complex because of the different first line. So first split all objects
        by splitting on a double new line. Then conver the first line into a list of ints. For the boards we use numpy
        from string to convert every board into a 1D array and then reshape it to become 2D again.
        """
        object_list = input_data.split("\n\n")
        drawn_numbers = [int(x) for x in object_list[0].split(",")]
        board_list = []
        for board in object_list[1:]:
            board_list.append(np.fromstring(board.replace("\n", " "), dtype="int", sep=" ").reshape(5, 5))
        return drawn_numbers, board_list

    def _solve_part1(self, parsed_data: tuple[list[int], list[np.ndarray]]) -> Any:
        """
        The overall solution is pretty straightforward and might not be the most computationally efficient, but it
        requires only a few lines of code. We create a mask containing ones for each board to keep track of the numbers
        that have been marked. By setting the drawn numbers to zero we can simply multiply the mask with the board at
        the end to get a sum of the unmarked numbers. We identify completed lines by summing along both axes: if a row
        or column only contains 0's, then the sum obviously will also only contain zeros. Once the first board completes
        , we return the solution.
        """
        drawn_numbers, board_list = parsed_data
        mask_list = [np.ones((5,5), dtype="byte") for x in range(len(board_list))]
        for number in drawn_numbers:
            for board_index in range(len(board_list)):
                mask_list[board_index][np.where(board_list[board_index] == number)] = 0
                if (mask_list[board_index].sum(axis=0) == 0).any() or (mask_list[board_index].sum(axis=1) == 0).any():
                    return (mask_list[board_index] * board_list[board_index]).sum() * number

    def _solve_part2(self, parsed_data: tuple[list[int], list[np.ndarray]]) -> Any:
        """
        Part 2 is very similar to part one. The only difference is that we need to remove (blacklist) all the boards
        that have been completed, otherwise they will pop-up more often (because other rows or columns) complete. We do
        not one to change the list we are iterating over in-place, so we blacklist the board index so we do not consider
        it again once we have completed it once. After all numbers have been draw we simply return the last board that
        was completed to solve part 2!
        """
        drawn_numbers, board_list = parsed_data
        mask_list = [np.ones((5,5), dtype="byte") for x in range(len(board_list))]
        last_board = None
        last_mask = None
        last_number = None
        blacklist = []
        for number in drawn_numbers:
            for board_index in range(len(board_list)):
                if board_index in blacklist:
                    continue
                mask_list[board_index][np.where(board_list[board_index] == number)] = 0
                if (mask_list[board_index].sum(axis=0) == 0).any() or (mask_list[board_index].sum(axis=1) == 0).any():
                    last_board = board_list[board_index]
                    last_mask = mask_list[board_index]
                    last_number = number
                    blacklist.append(board_index)
        return (last_board * last_mask).sum() * last_number
