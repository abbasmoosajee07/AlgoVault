"""i18n Puzzles - Puzzle 16
Solution Started: May 28, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/16
Solution by: Abbas Moosajee
Brief: [8-bit unboxing]
"""

#!/usr/bin/env python3

import os, re, copy, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
start_time = time.time()

# Load the input data from the specified file path
D16_file = "Day16_input.txt"
D16_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D16_file)

# Read and sort input data into a grid
with open(D16_file_path, encoding = "CP437") as file:
    input_data = file.read().strip().split('\n')

class PipesGame:
    def __init__(self, init_game):
        self.init_game = init_game
        self.init_grid, start_finish = self.__parse_grid(init_game)
        self.start, self.finish = start_finish
        self.grid_graph = self.__build_graph(self.init_grid)

    def __parse_grid(self, init_game):
        init_grid = {}
        start_symbol, finish_symbol = "▐▐ Start ▌▌", "▐▐ Finish ▌▌"
        start_coord, finish_coord = None, None
        for row_no, row_data in enumerate(init_game):
            if start_symbol in row_data:
                start_coord = (row_no, row_data.index(start_symbol) - 2)
            if finish_symbol in row_data:
                finish_coord = (row_no, row_data.index(finish_symbol) + len(finish_symbol) + 1)
            for col_no, cell in enumerate(row_data):
                init_grid[(row_no, col_no)] = cell

        start_coord = min(init_grid.keys()) if start_coord is None else start_coord
        finish_coord = max(init_grid.keys()) if finish_coord is None else finish_coord

        return init_grid, (start_coord, finish_coord)

    def __print_screen(self, game, visualize: bool = True):
        max_row, max_col= max(game.keys())

        # Construct screen grid
        screen_grid = [ ''.join(str(game.get((r, c), ' '))
            for c in range(max_col + 1)) for r in range(max_row + 1)
        ]

        if visualize: # Optionally visualize
            print('\n'.join(screen_grid))
            print('_' * (max_col + 1))
        return screen_grid

    def __build_graph(self, base_grid):
        graph = {}
        DIRECTIONS = {(0, 1):'>', (1, 0):'v', (-1, 0):'^', (0, -1):'<'}
        (MIN_ROW, MIN_COL), (MAX_ROW, MAX_COL) = (self.start, self.finish)
        for pos in base_grid.keys():
            row_no, col_no = pos
            for dr, dc in DIRECTIONS.keys():
                new_row, new_col = row_no + dr, col_no + dc
                if (MIN_ROW <= new_row <= MAX_ROW) and (MIN_COL <= new_col <= MAX_COL):
                    new_cell = self.init_grid[(new_row, new_col)]
                    if new_cell != " ":
                        graph.setdefault(pos, []).append((new_row, new_col))
        return graph

    def play_game(self, visualize: bool = False):
        self.rotations = 0

        self.__print_screen(self.init_grid)
        print(f"Start: {self.start} = {self.init_grid[self.start]} | Finish: {self.finish} = {self.init_grid[self.finish]}")
        # print(self.grid_graph[self.start], self.grid_graph[self.finish])
        # print(ord("┐"), chr(9488)) #┌, ┐, ┘, └
        return self.rotations

pipes = PipesGame(input_data)

rotations = pipes.play_game(True)
print("Rotations Required:", rotations)

print(f"Execution Time = {time.time() - start_time:.5f}s")
