"""
"""

from utils import Solution
from typing import Any
import numpy as np
import heapq


class DaySolution(Solution):
    def __init__(self, day: int = 15, year: int = 2021) -> None:
        super().__init__(day, year)

    def _parse_data(self, input_data: str) -> Any:
        """
        """
        return np.array([[int(x) for x in line] for line in input_data.split("\n") if line])

    def _dijkstra(self, grid: np.ndarray) -> int:
        node_list = [(0, (0, 0))]
        dist = np.full_like(grid, int(np.sum(grid)))
        dist[0, 0] = 0
        term_node = [x - 1 for x in grid.shape]
        visited = set()
        while node_list:
            # cur_node = node_list.pop(np.argmin(dist[[c[0] for c in node_list], [c[1] for c in node_list]]))
            cur_risk, cur_node = heapq.heappop(node_list)
            visited.add(cur_node)
            nbs = [(cur_node[0] + oy, cur_node[1] + ox) for oy, ox in [(-1, 0), (0, -1), (1, 0), (0, 1)] if
                   0 <= cur_node[0] + oy < dist.shape[0] and 0 <= cur_node[1] + ox < dist.shape[1]]
            for nb in nbs:
                if nb not in visited:
                    new_dist = dist[cur_node[0], cur_node[1]] + grid[nb[0], nb[1]]
                    if new_dist < dist[nb[0], nb[1]]:
                        dist[nb[0], nb[1]] = new_dist
                        heapq.heappush(node_list, (new_dist, nb))
            if cur_node == term_node:
                break
        return dist[term_node[0], term_node[1]]

    def _solve_part1(self, parsed_data: np.ndarray) -> int:
        """
        """
        return self._dijkstra(parsed_data)

    def _solve_part2(self, parsed_data: np.ndarray) -> int:
        """
        """
        column = np.vstack([parsed_data, parsed_data + 1, parsed_data + 2, parsed_data + 3, parsed_data + 4])
        generated_grid = np.hstack([column, column + 1, column + 2, column + 3, column + 4])
        generated_grid[np.where(generated_grid > 9)] -= 9
        return self._dijkstra(generated_grid)
