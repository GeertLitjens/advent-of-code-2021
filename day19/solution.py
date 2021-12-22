"""
"""

from utils import Solution
from typing import Any
import numpy as np
from collections import defaultdict, Counter

SWAP_AXES = np.array([[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0] , [2, 0, 1], [2, 1, 0]])
FLIPS = np.array([[1, 1, 1], [1, 1, -1], [1, -1, -1], [1, -1, 1], [-1, 1, 1], [-1, -1, 1],
         [-1, -1, -1], [-1, 1, -1]])


class DaySolution(Solution):
    def __init__(self, day: int = 19, year: int = 2021) -> None:
        super().__init__(day, year)
        self._paths = {}
        self._scanner_transforms = {}

    def _parse_data(self, input_data: str) -> Any:
        """
        """
        scanners = []
        scanners_unparsed = input_data.strip().split("\n\n")
        for i, scanner in enumerate(scanners_unparsed):
            coords = np.array([[int(x) for x in coord.split(",")]for coord in scanner.split("\n")[1:]])
            scanners.append({"coords": coords})
        return scanners

    def _get_transforms(self, scanners: Any) -> None:
        # Calculate distances
        if self._paths and self._scanner_transforms:
            return

        for scanner in scanners:
            coords = scanner["coords"]
            distances = []
            for c_1 in coords:
                coord_distances = []
                for c_2 in coords:
                    if (c_1 == c_2).all():
                        continue
                    coord_distances.append(np.abs(c_1[0] - c_2[0]) + np.abs(c_1[1] - c_2[1]) + np.abs(c_1[2] - c_2[2]))
                distances.append(coord_distances)
            scanner['distances'] = distances

        # Determine overlapping scanners
        matching_scanners = defaultdict(list)
        for i, s_1 in enumerate(scanners):
            d_1 = s_1["distances"]
            for j in range(i+1, len(scanners)):
                s_2 = scanners[j]
                overlap = False
                d_2 = s_2["distances"]
                for b_1_i, b_1 in enumerate(d_1):
                    if overlap:
                        break
                    for b_2_i, b_2 in enumerate(d_2):
                        nr_matches = len(list((Counter(b_1) & Counter(b_2)).elements()))
                        if nr_matches >= 11:
                            matching_scanners[i].append((j, b_1_i, b_2_i))
                            matching_scanners[j].append((i, b_2_i, b_1_i))
                            overlap = True
                            break

        path_tracker = []
        # Add first parts
        for scanner in matching_scanners.keys():
            if scanner == 0:
                continue
            current_path = [scanner]
            path_tracker.append(current_path)
        while path_tracker:
            current_path = path_tracker.pop()
            options = [x[0] for x in matching_scanners[current_path[-1]]]
            for option in options:
                if option == 0:
                    scanner = current_path[0]
                    comp_path = current_path + [option]
                    if current_path[0] in self._paths:
                        if len(comp_path) < len(self._paths[scanner]):
                            self._paths[scanner] = comp_path
                    else:
                        self._paths[scanner] = comp_path
                elif option not in current_path:
                    path_tracker.append(current_path + [option])

        for unmatched_scanner in sorted(self._paths, key=lambda x: len(self._paths[x])):
            cur_path = self._paths[unmatched_scanner]
            for f_s, t_s in zip(cur_path, cur_path[1:]):
                if f"{f_s}_{t_s}" not in self._scanner_transforms:
                    c_2_i, c_1_i = [x[1:] for x in matching_scanners[f_s] if x[0] == t_s][0]
                    match_found = False
                    for swap_axis in SWAP_AXES:
                        for flip in FLIPS:
                            trans_coords_c2 = (scanners[f_s]["coords"] * flip)[:, swap_axis]
                            c_1 = scanners[t_s]["coords"][c_1_i]
                            c_2 = trans_coords_c2[c_2_i]
                            offset = c_2 - c_1
                            new_coords = trans_coords_c2 - offset
                            hits = 0
                            for c_1 in scanners[t_s]["coords"]:
                                for c_2 in new_coords:
                                    if (c_1 == c_2).all():
                                        hits += 1
                                if hits > 11:
                                    match_found = True
                                    self._scanner_transforms[f"{f_s}_{t_s}"] = [swap_axis, flip, offset]
                                    break
                                if match_found:
                                    break
                            if match_found:
                                break
                        if match_found:
                            break

    def _solve_part1(self, parsed_data: Any) -> Any:
        """
        """

        self._get_transforms(parsed_data)
        for scanner, path in self._paths.items():
            for f_s, t_s in zip(path, path[1:]):
                swap_axis, flip, offset = self._scanner_transforms[f"{f_s}_{t_s}"]
                trans_coords = (parsed_data[scanner]["coords"] * flip)[:, swap_axis]
                parsed_data[scanner]["coords"] = trans_coords - offset
        unique_beacons = set()
        for scanner in parsed_data:
            for coord in scanner["coords"]:
                unique_beacons.add(tuple(coord))
        return len(unique_beacons)

    def _solve_part2(self, parsed_data: Any) -> Any:
        """
        """
        self._get_transforms(parsed_data)
        scanner_coords = np.array([[0, 0, 0]] * (len(self._paths) + 1))
        for scanner, path in self._paths.items():
            for f_s, t_s in zip(path, path[1:]):
                swap_axis, flip, offset = self._scanner_transforms[f"{f_s}_{t_s}"]
                trans_coords = (scanner_coords[scanner] * flip)[swap_axis]
                scanner_coords[scanner] = trans_coords - offset
        max_manhattan = 0
        for s_1 in scanner_coords:
            for s_2 in scanner_coords:
                manh_dist = np.abs(s_1 - s_2).sum()
                if manh_dist > max_manhattan:
                    max_manhattan = manh_dist
        return max_manhattan
