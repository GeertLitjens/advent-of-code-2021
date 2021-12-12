"""
"""

from utils import Solution
from typing import Any
from collections import defaultdict
import numpy as np


class DaySolution(Solution):
    def __init__(self, day: int = 12, year: int = 2021) -> None:
        super().__init__(day, year)

    def _parse_data(self, input_data: str) -> Any:
        """
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
                current_path_with_option = list(current_path)
                if option == "end":
                    current_path_with_option.append(option)
                    final_paths.append(current_path_with_option)
                elif option.isupper() or option not in current_path_with_option:
                    current_path_with_option.append(option)
                    path_tracker.append(current_path_with_option)
        return len(final_paths)

    def _solve_part2(self, parsed_data: dict[str, list[str]]) -> Any:
        """
        """
        class CavePath:
            def __init__(self):
                self.visited_twice = False
                self.path = ["start"]

        path_tracker = []
        final_paths = []
        # Add first parts
        for option in parsed_data["start"]:
            current_path = CavePath()
            current_path.path.append(option)
            path_tracker.append(current_path)
        while path_tracker:
            current_path = path_tracker.pop()
            options = parsed_data[current_path.path[-1]]
            for option in options:
                current_path_with_option = CavePath()
                current_path_with_option.path = list(current_path.path)
                current_path_with_option.visited_twice = current_path.visited_twice
                if option == "end":
                    current_path_with_option.path.append(option)
                    final_paths.append(current_path_with_option)
                elif option.isupper() or option not in current_path_with_option.path:
                    current_path_with_option.path.append(option)
                    path_tracker.append(current_path_with_option)
                elif not current_path.visited_twice and option != "start":
                    current_path_with_option.visited_twice = True
                    current_path_with_option.path.append(option)
                    path_tracker.append(current_path_with_option)
        return len(final_paths)
