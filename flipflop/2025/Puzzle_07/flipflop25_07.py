"""FlipFlop Codes Puzzles - Puzzle 07
Solution Started: July 16, 2026
Puzzle Link: https://flipflop.slome.org/2025/7
Solution by: Abbas Moosajee
Brief: [Hyper Grids]"""

#!/usr/bin/env python3
from pathlib import Path
from collections import defaultdict, deque
from math import factorial

# Load input file
input_file = "puzzle_07_input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()

class GridSolver:
    moves_2d = [(0,1), (0, -1), (1, 0), (-1, 0)]
    moves_3d = [
        (1, 0, 0), (-1, 0, 0),
        (0, 1, 0), (0, -1, 0),
        (0, 0, 1), (0, 0, -1),
    ]

    def __init__(self, grid_info):
        self.all_grids = [tuple(map(int, p.split(" "))) for p in grid_info]

    def find_path_count(self, start, end, grid, grid_3d = False):
        dist = {start: 0}
        ways = {start: 1}
        queue = deque([start])
        moves = self.moves_3d if grid_3d else self.moves_2d

        while queue:
            point = queue.popleft()
            for move in moves:
                if grid_3d:
                    dx, dy, dz = move
                    npoint = (point[0] + dx, point[1] + dy, point[2] + dz)
                else:
                    dx, dy = move
                    npoint = (point[0] + dx, point[1] + dy)
                if npoint not in grid:
                    continue

                if npoint not in dist:
                    dist[npoint] = dist[point] + 1
                    ways[npoint] = ways[point]
                    queue.append(npoint)
                elif dist[npoint] == dist[point] + 1:
                    ways[npoint] += ways[point]

        if end not in dist:
            return -1, 0
        return dist[end], ways[end]

    def solve_grids_2d(self):
        total = 0
        for (width, height)in self.all_grids:
            grid = [(row, col) for row in range(width) for col in range(height)]
            end = (width - 1, height - 1)
            step, count = self.find_path_count((0,0), end, grid)
            total += count
        return total

    def solve_grids_3d(self):
        total = 0
        for (width, height)in self.all_grids:
            grid = [(r, c, z) for r in range(width) for c in range(height) for z in range(width)]
            end = (width - 1, height - 1, width - 1)
            step, count = self.find_path_count((0,0,0), end, grid, True)
            total += count
        return total

    def solve_grids_nd(self):
        total = 0
        for (d, n)in self.all_grids:
            total += self.shortest_paths_count(d, n)
        return total

    @staticmethod
    def shortest_paths_count(d, n):
        steps_per_axis = n - 1
        total_steps = d * steps_per_axis
        return factorial(total_steps) // (factorial(steps_per_axis) ** d)


data1 = ['2 2', '3 3', '2 3']

grids = GridSolver(data)
print("FlipFlops 25, Puzzle 07")
print("Part 1:", grids.solve_grids_2d())
print("Part 2:", grids.solve_grids_3d())
print("Part 3:", grids.solve_grids_nd())

