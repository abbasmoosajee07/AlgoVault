"""Codyssi Puzzles - Problem 10
Solution Started: Apr 12, 2025
Puzzle Link: https://www.codyssi.com/view_problem_14?
Solution by: Abbas Moosajee
Brief: [Cyclops Chaos]
"""

#!/usr/bin/env python3

import os, re, copy, time, heapq
import numpy as np
start_time = time.time()

# Load the input data from the specified file path
D10_file = "Day10_input.txt"
D10_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D10_file)

# Read and sort input data into a grid
with open(D10_file_path) as file:
    input_data = file.read().strip().split('\n')
    input_grid = [list(map(int, line.split())) for line in input_data]

class CyclopsGrid:
    def __init__(self, init_grid: list[list[int]]):
        self.base_grid = init_grid
        self.grid_dict = {
            (row_no, col_no): int(cell)
            for row_no, row_data in enumerate(init_grid, start=1)
            for col_no, cell in enumerate(row_data, start=1)
        }
        self.GRID_SIZE = max(self.grid_dict.keys())
        self.graph = self.build_graph(self.grid_dict)

    @staticmethod
    def print_grid(grid_dict: dict, movements: list = []):
        min_row, min_col = min(grid_dict.keys())
        max_row, max_col = max(grid_dict.keys())

        grid_list = []

        for row_no in range(min_row, max_row + 1):
            row = ''
            for col_no in range(min_col, max_col + 1):
                pos = (row_no, col_no)

                if pos in movements:
                    row += '█' if '█'.encode().decode('utf-8', 'ignore') else '|'

                elif pos in grid_dict.keys():
                    row += str(grid_dict[pos])
                else:
                    row += '.'

            grid_list.append(row)

        # Print grid
        print("\n".join(grid_list))
        print('_' * len(grid_list[-1]))

    @staticmethod
    def build_graph(grid_dict: dict) -> dict:
        DIRECTIONS = {(0, 1):'>', (1, 0):'v',
                        # (-1, 0):'^', (0, -1):'<'
                    }
        graph_dict = {}

        for (row, col) in grid_dict:
            adj_cells = []
            for dr, dc in DIRECTIONS:
                nr, nc = row + dr, col + dc
                next_pos = (nr, nc)
                if next_pos in grid_dict:
                    adj_cells.append(next_pos)
            graph_dict[(row, col)] = adj_cells

        return graph_dict

    def find_safest_path_basic(self, start: tuple, goal: tuple, visualize: bool = False) -> dict:
        """
        Find safest path through the grid without heapq, but allows for visualisation
        """
        grid_dict = self.grid_dict
        graph = self.graph

        # Queue of (path, total_safety)
        queue = [([start], grid_dict[start])]
        visited = {start: grid_dict[start]}

        best_path, best_safety= ([], float('inf'))

        while queue:
            path, safety = queue.pop(0)
            current = path[-1]

            if current == goal:
                if safety < best_safety:
                    best_safety = safety
                    best_path = path
                if visualize:
                    print(f"\nSafety Level:{best_safety}")
                    self.print_grid(grid_dict, updated_path)
                continue

            for neighbor in graph.get(current, []):
                if neighbor in path:
                    continue  # avoid cycles

                new_safety = safety + grid_dict[neighbor]
                updated_path = path + [neighbor]

                if neighbor not in visited or new_safety < visited[neighbor]:
                    visited[neighbor] = new_safety
                    queue.append((updated_path, new_safety))

        return {pos: grid_dict[pos] for pos in best_path}

    def find_safest_path_heapq(self, start: tuple, goal: tuple) -> dict:
        """
        Find safest path through the grid using heapq to improve processing,
        20x faster than `find_safest_path_basic`
        """
        grid_dict = self.grid_dict
        graph = self.graph

        # Priority queue: (total_safety_cost, current_path)
        heap = [(grid_dict[start], [start])]
        visited = {}

        while heap:
            safety, path = heapq.heappop(heap)
            current = path[-1]

            # If we've visited with a lower safety cost before, skip
            if current in visited and visited[current] <= safety:
                continue
            visited[current] = safety

            if current == goal:
                return {pos: grid_dict[pos] for pos in path}

            for neighbor in graph.get(current, []):
                if neighbor not in path:  # avoid cycles
                    new_path = path + [neighbor]
                    new_safety = safety + grid_dict[neighbor]
                    heapq.heappush(heap, (new_safety, new_path))

        return {}  # No path found

cyclops = CyclopsGrid(input_grid)
min_safety = min(np.sum(cyclops.base_grid, axis=num).min() for num in [0, 1])
print("Part 1:", min_safety)

safest_path_p2 = cyclops.find_safest_path_heapq((1, 1), (15, 15))
print("Part 2:", sum(safest_path_p2.values()))

safest_path_p3 = cyclops.find_safest_path_heapq((1, 1), cyclops.GRID_SIZE)
print("Part 3:", sum(safest_path_p3.values()))

# print(f"Execution Time = {time.time() - start_time:.5f}")
