"""
Interesting graphical puzzle in the end, the first one where I could not auto-submit Part 2 but had to type it in
manually. In the end I took the intellectually easy way output by not actually mirroring the coordinates, but simply
using a very large numpy array to holds all the positions and simply using np.flip and appropriate indexing to do the
folds, which worked well enough.
"""

from utils import Solution
from typing import Any
import numpy as np


class DaySolution(Solution):
    def __init__(self, day: int = 13, year: int = 2021) -> None:
        super().__init__(day, year)

    def _parse_data(self, input_data: str) -> Any:
        """
        More involved data parsing function this time around because I wanted to encode the coordinates in an array.
        So first split the coordinates and the folding instructions. Then generate an array as large as the span of the
        coordinates in both dimensions and set the coordinates to 1. Subsequently, split the fold instructions into an
        axis identifier and a position.
        """
        coord_string, fold_string = input_data.split("\n\n")
        coords = np.array([[int(coord.split(",")[1]), int(coord.split(",")[0])] for coord in coord_string.split("\n")])
        paper = np.zeros((np.max(coords[:, 0]) + 1, np.max(coords[:, 1]) + 1), dtype="ubyte")
        paper[coords[:, 0], coords[:, 1]] = 1
        folds = [(a_p.split("=")[0].split("fold along ")[1], int(a_p.split("=")[1])) for a_p in fold_string.split("\n") if a_p]
        return paper, folds

    def _solve_part1(self, parsed_data: Any) -> Any:
        """
        Part 1 uses the basic folding mechanism: identify the axis and flip the subarray to the right or bottom and add
        that to the subarray to the left or top and removing the remainder. Here we just take the first fold.
        """
        paper, folds = parsed_data
        axis, pos = folds[0]
        if axis == "x":
            paper = paper[:, :pos] + np.flip(paper[:, pos + 1:], axis=1)
        else:
            flipped = np.flip(paper[pos + 1:] , axis=0)
            paper = paper[:pos] + flipped
        paper = (paper > 0).astype("ubyte")
        return np.sum(paper)

    def _solve_part2(self, parsed_data: Any) -> Any:
        """
        Same as part 1, but now we do all folds. Because I don't want to implement an entire OCR step, I just read the
        result from the terminal window. To still have a meaningful test, I use the same return value as in part 1.
        """
        paper, folds = parsed_data
        for axis, pos in folds:
            if axis == "x":
                paper = paper[:, :pos] + np.flip(paper[:, pos + 1:], axis=1)
            else:
                flipped = np.flip(paper[pos + 1:] , axis=0)
                paper = paper[:pos] + flipped
            paper = (paper > 0).astype("ubyte")
        print("\n" + np.array2string(paper, separator='', formatter={'int': {0: ' ', 1: "\u2588"}.get}))
        return np.sum(paper)
