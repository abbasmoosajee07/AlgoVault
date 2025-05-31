"""i18n Puzzles - Puzzle 16
Solution Started: May 28, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/16
Solution by: Abbas Moosajee
Brief: [8-bit unboxing]
"""

#!/usr/bin/env python3

import os, re, copy, time, click
from collections import defaultdict
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
start_time = time.time()

# Load the input data from the specified file path
D16_file = "Day16_input1.txt"
D16_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D16_file)

# Read and sort input data into a grid
with open(D16_file_path, encoding = "CP437") as file:
    input_data = file.read().strip().split('\n')

class PipesGame:
    DIRECTIONS = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}

    VALID_SYMBOLS = list("┘─└║│┤┌╚╫┬├╞┐╔╝╡┴╩╗╬╣┼╢╥╨═╧╦╠╪╤╟")

    def __init__(self, init_game):
        self.init_grid, (self.start, self.finish) = self.__parse_grid(init_game)
        self.grid_graph = self.__build_graph(self.init_grid)

    def __parse_grid(self, init_game):
        grid, start, finish = {}, None, None
        start_marker, finish_marker = "▐▐ Start ▌▌", "▐▐ Finish ▌▌"

        for r, line in enumerate(init_game):
            if start_marker in line:
                start = (r, line.index(start_marker) - 2)
            if finish_marker in line:
                finish = (r, line.index(finish_marker) + len(finish_marker) + 1)
            for c, char in enumerate(line):
                grid[(r, c)] = char

        start = min(grid) if start is None else start
        finish = max(grid) if finish is None else finish
        return grid, (start, finish)

    def __print_grid(self, grid, visualize=True):
        (min_r, min_c), (max_r, max_c) = min(grid), max(grid)
        screen = [
            ''.join(str(grid.get((r, c), ' ')) for c in range(min_c, max_c + 1))
            for r in range(min_r, max_r + 1)
        ]
        if visualize:
            print('\n'.join(screen))
            print('_' * (max_c + 1))
        return '\n'.join(screen)

    def __print_screen(self, grid, control, pos=(0, 0)):
        bold_map = {
            ' ': '▮', '─': '━', '═': '━', '│': '┃', '║': '┃',
            '┌': '┏', '╔': '┏', '┐': '┓', '╗': '┓', '└': '┗',
            '╚': '┗', '┘': '┛', '╝': '┛', '┬': '┳', '╦': '┳',
            '╤': '┳', '╥': '┳', '┴': '┻', '╩': '┻', '╧': '┻',
            '╨': '┻', '├': '┣', '╠': '┣', '╞': '┣', '╟': '┣',
            '┼': '╋', '╬': '╋', '╪': '╋', '╫': '╋', '┤': '┫',
            '╣': '┫', '╡': '┫', '╢': '┫'
        }
        num_cols = max(grid)[1] + 1
        full_screen = []
        if control == "Numbers":
            first = '  ' + ''.join(str(i // 10) for i in range(num_cols))
            second = '  ' + ''.join(str(i % 10) for i in range(num_cols))
            full_screen.extend([first, second])
            display = copy.deepcopy(grid)
            display[pos] = bold_map.get(display[pos], display[pos])
            lines = self.__print_grid(display, False).split('\n')
            for i, line in enumerate(lines):
                print_line = f"{str(i).zfill(2)}{line}{str(i).zfill(2)}"
                full_screen.append(print_line)
            full_screen.extend([first, second])
            print('\n'.join(full_screen))

        elif control == "Arrows":
            display = copy.deepcopy(grid)
            display[pos] = bold_map.get(display[pos], display[pos])
            full_screen = self.__print_grid(display)

    def __build_graph(self, grid):
        graph = {}
        (min_r, min_c), (max_r, max_c) = self.start, self.finish
        for (r, c), val in grid.items():
            if min_r <= r <= max_r and min_c <= c <= max_c:
                for dr, dc in self.DIRECTIONS.values():
                    nr, nc = r + dr, c + dc
                    if min_r <= nr <= max_r and min_c <= nc <= max_c:
                        if grid.get((nr, nc)) in self.VALID_SYMBOLS:
                            graph.setdefault((r, c), set()).add((nr, nc))
        return graph

    def __rotate_pipe(self, pos, grid, rotations):
        rotation_map = {
            '┼': ('┼', 1), '╫': ('╪', 1), '╪': ('╫', 1),
            '─': ('│', 1), '│': ('─', 1), '═': ('║', 1), '║': ('═', 1),
            '┌': ('┐', 3), '┐': ('┘', 3), '╔': ('╗', 3), '╗': ('╝', 3),
            '└': ('┌', 3), '┘': ('└', 3), '╚': ('╔', 3), '╝': ('╚', 3),
            '├': ('┬', 3), '┤': ('┴', 3), '╠': ('╦', 3), '╣': ('╩', 3),
            '┬': ('┤', 3), '┴': ('├', 3), '╦': ('╣', 3), '╩': ('╠', 3),
            '╞': ('╥', 3), '╡': ('╨', 3), '╧': ('╟', 3), '╤': ('╢', 3),
            '╥': ('╡', 3), '╨': ('╞', 3), '╟': ('╤', 3), '╢': ('╧', 3)
        }

        char = grid[pos]
        new_char, mod = rotation_map.get(char, (char, 0))
        rotations[pos] = (rotations[pos] + 1) % (mod + 1)
        grid[pos] = new_char
        return rotations, grid

    def play_game_auto(self, visualize=False):
        print(f"Start: {self.start} = {self.init_grid[self.start]} | Finish: {self.finish} = {self.init_grid[self.finish]}")
        queue, all_rots = [(0, self.init_grid.copy(), self.start)], [0]

        while queue:
            rots, grid, current = queue.pop(0)
            if current == self.finish:
                all_rots.append(rots)
            else:
                grid = self.__rotate_pipe(current, grid)
                if visualize:
                    self.__print_grid(grid)

        print(self.VALID_SYMBOLS)
        return min(all_rots)

    def play_game_manually(self, control="Arrows"):
        grid = self.init_grid.copy()
        rotations_dict = defaultdict(lambda: 0)
        row, col = self.start
        max_r, max_c = self.finish[0] + 1, self.finish[1] + 1

        if control == "Numbers":
            while True:
                self.__print_screen(grid, control, (row, col))
                print("Current Rotation Count:", sum(rotations_dict.values()))
                string = input('Enter row, col or "q" to quit: ')
                if string == 'q':
                    break
                try:
                    row, col = map(int, string.split(','))
                    rotations_dict, grid = self.__rotate_pipe((row, col), grid, rotations_dict)
                except:
                    print('Invalid input. Try again.')

        elif control == "Arrows":
            while True:
                self.__print_screen(grid, control, (row, col))
                print("Current Rotation Count:", sum(rotations_dict.values()))
                click.echo('Use arrow keys or space to rotate, q to quit')
                key = click.getchar()
                if key == '\xe0H'  : row = (row - 1) % max_r
                elif key == '\xe0P': row = (row + 1) % max_r
                elif key == '\xe0K': col = (col - 1) % max_c
                elif key == '\xe0M': col = (col + 1) % max_c
                elif key == ' ':  # space
                    rotations_dict, grid = self.__rotate_pipe((row, col), grid, rotations_dict)
                elif key == 'q':
                    break
                else:
                    print(f'Key {key} not recognized')

        return sum(rotations_dict.values())

pipes = PipesGame(input_data)

rotations = pipes.play_game_manually("Arrows")
# rotations = pipes.play_game_auto(True)
print("Rotations Required:", rotations)


print(f"Execution Time = {time.time() - start_time:.5f}s")

# └──┐     ┘┬┐
# └──┘     ─││
# └─│││──┘τ┘┘│
# ■┌╞──│─┐  ┘┐
#  ─═╔╔┌│─│─┴┐
#  │═╗╠│½    │
# ┌┘╗║╝─°    │
# └──││┐     │

# └──┐     ┌┬┐
# ┌──┘     │││
# └──────┐τ└┘│
# ■┌╥────┘  ┌┘
#  │║╔╗┌────┴┐
#  │║╚╣│½    │
# ┌┘╚═╝│°    │
# └────┘     │

