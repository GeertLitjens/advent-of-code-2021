"""
This day was slightly more challenging. Initially, I thought I might need to apply some binary arithmetic to solve
this problem, however, in the end this was not needed. I did decide to use numpy for fast and easy handling of arrays.
Potentially there is a smarter/faster/code-efficient solution that I didn't think of, but what I came up with works, so
that is the most important part.
"""

from utils import Solution
from typing import Any
import numpy as np


class DaySolution(Solution):
    def __init__(self, day: int = 3, year: int = 2021) -> None:
        super().__init__(day, year)

    def _parse_data(self, input_data: str) -> Any:
        """
        The parsing of the data was slightly different than previous days. First, I convert the dataset to a list of
        lists containing string which I convert to a numpy array.
        """
        string_list = [list(x) for x in input_data.split("\n") if x]
        string_array = np.array(string_list)
        return string_array

    def _solve_part1(self, parsed_data: np.ndarray) -> Any:
        """
        Because I converted the data to a numpy array, I can easily perform operations along any dimension.
        Specifically, to identify the most common element for each bit, I take the ceil of the median across the rows.
        The median itself in a binary setting will simply select the most common element, and the np.ceil resolves ties
        by assigning them to 1. Then I use a list comprehension to invert the resultant string to get the least common
        bits. Last, I convert the bit string to an integer by calling int with a base of 2.
        """
        median = np.ceil(np.median(parsed_data.astype("int"), axis=0)).astype("int")
        most_common = "".join(list(median.astype('str')))
        least_common = "".join(['1' if i == '0' else '0' for i in most_common])
        gamma = int(most_common, 2)
        epsilon = int(least_common, 2)
        return gamma * epsilon

    def _solve_part2(self, parsed_data: np.ndarray) -> Any:
        """
        Again, reading the actual task was the most challenging part here for me. Initially I assumed I could simply
        use the most and least common bit strings from the previous example, however, then I realized that I had to do
        it per bit because the bit strings needed to be calculated with respect to the remaining rows. The filtering on
        the bit criteria is very easy to do in numpy using logical expression. I could very well imagine that this
        problem can be solved more efficiently with a recurrent function or so, but my approach is still reasonably
        fast (6 - 7 ms), so I think it is ok.
        """
        filtered_data = parsed_data.copy().astype("int")
        i = 0
        while filtered_data.shape[0] > 1:
            el = int(np.ceil(np.median(filtered_data[:, i])))
            filtered_data = filtered_data[filtered_data[:, i] == el]
            i += 1
        og_rating = int("".join(filtered_data[0].astype("str")), 2)
        filtered_data = parsed_data.copy().astype("int")
        i = 0
        while filtered_data.shape[0] > 1:
            el = int(np.abs(np.median(filtered_data[:, i]) - 1))
            filtered_data = filtered_data[filtered_data[:, i] == el]
            i += 1
        co_rating = int("".join(filtered_data[0].astype("str")), 2)
        return og_rating * co_rating
