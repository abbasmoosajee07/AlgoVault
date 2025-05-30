"""i18n Puzzles - Puzzle 16
Solution Started: May 28, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/16
Solution by: Abbas Moosajee
Brief: [8-bit unboxing]
"""

#!/usr/bin/env python3

import os, re, copy, time, random
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
    DIRECTIONS = {(0, 1):'>', (1, 0):'v', (-1, 0):'^', (0, -1):'<'}
    VALID_SYMBOLS = list("┘─└║│┤┌╚╫┬├╞┐╔╝╡┴╩╗╬╣┼╢╥╨═╧╦╠╪╤╟")

    def __init__(self, init_game):
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
        min_row, min_col= min(game.keys())
        max_row, max_col= max(game.keys())

        # Construct screen grid
        screen_grid = [ ''.join(str(game.get((r, c), ' '))
            for c in range(min_col, max_col + 1))
            for r in range(min_row, max_row + 1)
        ]

        if visualize: # Optionally visualize
            print('\n'.join(screen_grid))
            print('_' * (max_col + 1))
        return screen_grid

    def __build_graph(self, base_grid):
        graph = {}
        (MIN_ROW, MIN_COL), (MAX_ROW, MAX_COL) = (self.start, self.finish)
        for pos in base_grid.keys():
            row_no, col_no = pos
            if (MIN_ROW <= row_no <= MAX_ROW) and (MIN_COL <= col_no <= MAX_COL):
                for dr, dc in self.DIRECTIONS.keys():
                    new_row, new_col = row_no + dr, col_no + dc
                    if (MIN_ROW <= new_row <= MAX_ROW) and (MIN_COL <= new_col <= MAX_COL):
                        new_cell = self.init_grid[(new_row, new_col)]
                        if new_cell in self.VALID_SYMBOLS:
                            graph.setdefault(pos, set()).add((new_row, new_col))
        return graph

    def __rotate_pipe(self, pos, grid):
        CONNECTIONS = {
            "─": ("─", "┐"), # horizontal and vertical pipes
        }
        # Manual rotation map (90-degree clockwise)
        CW_ROTATION = {
            "│": "─", "─": "│", "║": "═", "═": "║",
            "┌": "┐", "┐": "┘", "┘": "└", "└": "┌",
            "┬": "┤", "┤": "┴", "┴": "├", "├": "┬",
            "╔": "╗", "╗": "╝", "╝": "╚", "╚": "╔",
            "╞": "╥", "╥": "╡", "╡": "╨", "╨": "╞",
            "╣": "╩", "╩": "╠", "╠": "╦", "╦": "╣",
            "╫": "╪", "╪": "╫",  # alternate cross-style rotation
            "╬": "╬", "╢": "╢", "╟": "╟", "┼": "┼",  # symmetric
            "╧": "╤", "╤": "╧",  # If applicable
        }

        rotation_dict = {
            ' ': (' ',1), '─': ('│',2), '│': ('─',2),
            '┌': ('┐',4),
            '┐': ('┘',4),
            '└': ('┌',4),
            '┘': ('└',4),
            '├': ('┬',4),
            '┤': ('┴',4),
            '┬': ('┤',4),
            '┴': ('├',4),
            '┼': ('┼',1),
            }
        def get_clockwise_rotations(symbol):
            rotations = [symbol]
            for _ in range(3):
                next_symbol = CW_ROTATION.get(rotations[-1], rotations[-1])
                rotations.append(next_symbol)
            return rotations

        adjacent = self.grid_graph[pos]
        # for adj_pos in adjacent:
        #     sym = self.init_grid[adj_pos]
        #     rot_sym = get_clockwise_rotations(sym)
        #     print(adj_pos, sym, rot_sym)
        sym = "╬"
        print(sym, get_clockwise_rotations(sym))
        # sym = "┘"
        # print(sym, get_clockwise_rotations(sym))
        # sym = "┐"
        # print(sym, get_clockwise_rotations(sym))
        print(set(CW_ROTATION.keys()) - set(self.VALID_SYMBOLS))
        return grid

    def play_game(self, visualize: bool = False):
        self.rotations = 0
        start, finish = self.start, self.finish

        print(f"Start: {start} = {self.init_grid[start]} | Finish: {finish} = {self.init_grid[finish]}")
        queue = [(0, self.init_grid.copy(), start)]
        all_rotations = [0]
        while queue:
            rots, grid, current = queue.pop(0)
            if current == finish:
                all_rotations.append(rots)
            else:
                grid = self.__rotate_pipe(current, grid)
                if visualize:
                    self.__print_screen(grid)
        print(self.VALID_SYMBOLS)
        return min(all_rotations)

pipes = PipesGame(input_data)

rotations = pipes.play_game(True)
print("Rotations Required:", rotations)

# Define pipe pieces with rotatable variants (rotations in clockwise order)
pipe_variants = {
    '─': ['─', '│'],
    '┌': ['┌', '┐', '┘', '└'],
    '└': ['└', '┌', '┐', '┘'],
    '┐': ['┐', '┘', '└', '┌'],
    '┘': ['┘', '└', '┌', '┐'],
    '│': ['│', '─'],
    # Add more complex tiles if desired
}

# Start with a basic tile set
tiles = list(pipe_variants.keys())

# Directions map (for traversal)
DIRS = {
    '^': (-1, 0),
    'v': (1, 0),
    '<': (0, -1),
    '>': (0, 1),
}

# Connection map for each tile
connections = {
    '─': ['<', '>'],
    '│': ['^', 'v'],
    '┌': ['>', 'v'],
    '└': ['^', '>'],
    '┐': ['<', 'v'],
    '┘': ['^', '<'],
    # Add more complex pieces as needed
}

def rotate(tile):
    if tile in pipe_variants:
        variants = pipe_variants[tile]
        idx = variants.index(tile)
        return variants[(idx + 1) % len(variants)]
    return tile

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_grid(grid):
    for row in grid:
        print(' '.join(row))
    print()

def is_connected(pipe1, dir1, pipe2, dir2):
    return dir1 in connections.get(pipe1, []) and dir2 in connections.get(pipe2, [])

def get_opposite(dir):
    return {'^': 'v', 'v': '^', '<': '>', '>': '<'}[dir]

def dfs(grid, x, y, visited):
    stack = [(x, y)]
    while stack:
        cx, cy = stack.pop()
        if (cx, cy) in visited:
            continue
        visited.add((cx, cy))
        pipe = grid[cx][cy]
        for d in connections.get(pipe, []):
            dx, dy = DIRS[d]
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                neighbor = grid[nx][ny]
                if is_connected(pipe, d, neighbor, get_opposite(d)):
                    stack.append((nx, ny))
    return visited

def game_loop():
    rows, cols = 5, 5
    grid = [[random.choice(tiles) for _ in range(cols)] for _ in range(rows)]

    start = (0, 0)
    end = (rows - 1, cols - 1)
    grid[start[0]][start[1]] = '┌'
    grid[end[0]][end[1]] = '┘'

    while True:
        clear_screen()
        print("Pipe Game: Connect Start (S) to Goal (G)!\n")
        for i, row in enumerate(grid):
            print(' '.join(
                ('S' if (i, j) == start else 'G' if (i, j) == end else cell)
                for j, cell in enumerate(row)
            ))
        print("\nEnter tile to rotate as 'row col' (or 'q' to quit):")
        cmd = input(">> ").strip()
        if cmd == 'q':
            break
        try:
            r, c = map(int, cmd.split())
            grid[r][c] = rotate(grid[r][c])
        except:
            continue

        visited = dfs(grid, start[0], start[1], set())
        if end in visited:
            clear_screen()
            display_grid(grid)
            print("🎉 You connected the pipes! Well done!")
            break

# if __name__ == '__main__':
#     game_loop()

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