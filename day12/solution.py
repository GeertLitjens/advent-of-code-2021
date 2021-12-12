"""
Interesting problem today, sort of a population growth model almost, with exponential growth of paths at the beginning
and subsequently they go down after hitting end. Adding new paths happens through iterating all the option in a loop
until you hit the blocking conditions (end or double access to lowercase cave). Part 2 added an interesting wrinkle, but
in the end only a small addition is needed.
"""

from utils import Solution
from typing import Any
from collections import defaultdict


class DaySolution(Solution):
    def __init__(self, day: int = 12, year: int = 2021) -> None:
        super().__init__(day, year)

    def _parse_data(self, input_data: str) -> Any:
        """
        Slightly more interesting parser than most days. Here I use a defaultdict to create a mapping betwene the nodes,
         for each entry I store the connected chambers. Note that all of them are bidirectional, so a-b is also b-a.
        """
        cave_mapper = defaultdict(list)
        for line in input_data.split("\n"):
            if line:
                start_node, end_node = line.split("-")
                cave_mapper[start_node].append(end_node)
                cave_mapper[end_node].append(start_node)
        return cave_mapper

    def _solve_part1(self, parsed_data: dict[str, list[str]]) -> Any:
        """
        Part 1 required some thought, but in the end it was just adding each option to a running list of open paths. As
        soon as you hit the end point, add it to final paths. The only thing that is a bit special is that we only add
        an option if it is not already in the path or if it is uppercase (e.g. large cave).
        """
        path_tracker = []
        final_paths = []
        # Add first parts
        for option in parsed_data["start"]:
            current_path = ["start", option]
            path_tracker.append(current_path)
        while path_tracker:
            current_path = path_tracker.pop()
            options = parsed_data[current_path[-1]]
            for option in options:
                if option == "end":
                    final_paths.append(current_path + [option])
                elif option.isupper() or option not in current_path:
                    path_tracker.append(current_path + [option])
        return len(final_paths)

    def _solve_part2(self, parsed_data: dict[str, list[str]]) -> Any:
        """
        Small extension to part 1, we now also keep track whether a path has visited a small cave twice. If not, then we
        can add lowercase options. Other than that, exactly the same as part 1.
        """
        path_tracker = []
        final_paths = []
        for option in parsed_data["start"]:
            path_tracker.append({"path": ["start", option], "twice": False})
        while path_tracker:
            current_path = path_tracker.pop()
            options = parsed_data[current_path["path"][-1]]
            for option in options:
                if option == "end":
                    final_paths.append({"path": current_path["path"] + [option], "twice": current_path["twice"]})
                elif option.isupper() or option not in current_path["path"]:
                    path_tracker.append({"path": current_path["path"] + [option], "twice": current_path["twice"]})
                elif not current_path["twice"] and option != "start":
                    path_tracker.append({"path": current_path["path"] + [option], "twice": True})
        return len(final_paths)
