"""
Good old Dijkstra's algorithm, this was very familiar to me. I decided not to use the scipy implementation, but to
implement it myself again. I had something that worked really quickly, but finding the node with minimum distance to the
source at each step was very slow. This is when I discovered Python actually has a heapq that keeps track of the lowest
value, which was supernice and efficient. That made my lazy solution for part 2 actually computationally tractable (I
simply increase the grid). A nice solution would have been to simply wrap the position back to the current grid and add
the multiplicty (e.g. 24 wraps to 4 while adding 4 to the risk). But I ran out of time and took the easy way out :).
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
        Data parsing was trivial, simply convert the text to a numpy array as done before many times.
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
        Simple implementation of Dijkstra's algorithm where the risk scores are considered as node distances.
        We simply define the source and terminal nodes and a distance matrix to keep track of the distance. Last, for
        computational efficiency, we keep use a separate set of visited nodes so we don't recompute distances
        unnecessarily. The key thing I learned later was that Python has the heapq package, which provides you with
        a minimum tracking queue, which helps a lot in speedily finding the current minimum distance node. The last part
        is simply returning the distance once we reach the terminal.
        """
        return self._dijkstra(parsed_data)

    def _solve_part2(self, parsed_data: np.ndarray) -> int:
        """
        Lazy solution: simply expand the grid in horizontal and vertical direction and run Dijkstra's algorithm on the
        expanded grid. I wrap the values larger than 9.
        """
        column = np.vstack([parsed_data, parsed_data + 1, parsed_data + 2, parsed_data + 3, parsed_data + 4])
        generated_grid = np.hstack([column, column + 1, column + 2, column + 3, column + 4])
        generated_grid[np.where(generated_grid > 9)] -= 9
        return self._dijkstra(generated_grid)
