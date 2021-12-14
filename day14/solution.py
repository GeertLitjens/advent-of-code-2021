"""
The most challenging puzzle for me so far, obviously mostly part 2. I made a simple, straighforward list iterator for
part 1, but of course that could not handle 2^40 elements in part 2. So I had to rethink my strategy and it took me a
bit of time to realize that I could just keep track again of only the pairs and the number of pairs as their positions
do not matter. So I used the Python Counter class for that, which is essentially a fancy dictionary structure. I left my
old solution for part 1, just to show how you can do it in a very computationally inefficient wat as well :).
"""

from utils import Solution
from typing import Any
from collections import Counter


class DaySolution(Solution):
    def __init__(self, day: int = 14, year: int = 2021) -> None:
        super().__init__(day, year)

    def _parse_data(self, input_data: str) -> Any:
        """
        Again data consists of two parts, so first split on a double new line and turn the template string into a list.
        Then parse the rules into a dictionary.
        """
        template, rules_string = input_data.split("\n\n")
        template = [x for x in template]
        rules = {}
        for line in rules_string.split("\n"):
            if line:
                k, v = line.split(" -> ")
                rules[k] = v
        return template, rules

    def _solve_part1(self, parsed_data: Any) -> Any:
        """
        Part 1 just work directly on lists. Iterate over the old list, a the first element of a pair  and a new element
        to the new list based on the rules. This works well and fast, however it does not scale to a large number of
        turns as the length of the list grows exponentially.
        """
        old_poly, rules = parsed_data
        for step in range(10):
            new_poly = []
            for e_i in range(len(old_poly) - 1):
                new_poly.append(old_poly[e_i])
                new_poly.append(rules[old_poly[e_i] + old_poly[e_i + 1]])
            new_poly.append(old_poly[-1])
            old_poly = new_poly
        cntr = Counter(new_poly)
        counts = cntr.most_common()
        return counts[0][1] - counts[-1][1]

    def _solve_part2(self, parsed_data: Any) -> Any:
        """
        Smarter solution: we only keep track of the pairs and how often they occur. Then at each step, iterate over all
        the pairs, remove the originals and replace them with two new ones pased on the rules. Last trick is to keep a
        separate counter to actually count then number of individual elements so we don't have to figure that out from
        the pair counter at the end.
        """
        old_poly, rules = parsed_data
        poly_dict = Counter(map(str.__add__, old_poly, old_poly[1:]))
        elem_count = Counter(old_poly)
        for step in range(40):
            for (elem_1, elem_2), count in poly_dict.copy().items():
                new_elem = rules[elem_1 + elem_2]
                poly_dict[elem_1 + elem_2] -= count
                poly_dict[elem_1 + new_elem] += count
                poly_dict[new_elem + elem_2] += count
                elem_count[new_elem] += count
        return max(elem_count.values()) - min(elem_count.values())
