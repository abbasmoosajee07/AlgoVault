"""i18n Puzzles - Puzzle 16
Solution Started: May 28, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/16
Solution by: Abbas Moosajee
Brief: [8-bit unboxing]
"""

#!/usr/bin/env python3

import os, re, copy, time, click
from collections import defaultdict, deque
start_time = time.time()

# Load the input data from the specified file path
D16_file = "Day16_input1.txt"
D16_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D16_file)

# Read and sort input data into a grid
with open(D16_file_path, encoding = "CP437") as file:
    input_data = file.read().strip().split('\n')

class PipesGame:
    REMOTE_CONTROL = {1: "Numbers", 2: "Arrows", 3: "Auto"}
    REVERSE_DIR = { '^': 'v', 'v': '^', '<': '>', '>': '<'}
    DIRECTIONS = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}
    VALID_SYMBOLS = list("╕╫╞─╒╠╓┘├═╩╔╖╗┬┤╙┴╢╚╪╦└┌╧║╜╣│╘╟╡╛┼╥╬┐╨╤╝")
    PIPE_CONNECTIONS = {
        '═': {'<', '>'}, '─': {'<', '>'},
        '║': {'^', 'v'}, '│': {'^', 'v'},
        '┌': {'>', 'v'}, '┐': {'<', 'v'},
        '└': {'>', '^'}, '┘': {'<', '^'},
        '╔': {'>', 'v'}, '╗': {'<', 'v'},
        '╚': {'>', '^'}, '╝': {'<', '^'},
        '├': {'^', 'v', '>'}, '┤': {'^', 'v', '<'},
        '╞': {'^', 'v', '>'}, '╡': {'^', 'v', '<'},
        '╟': {'^', 'v', '>'}, '╢': {'^', 'v', '<'},
        '╠': {'^', 'v', '>'}, '╣': {'^', 'v', '<'},
        '┬': {'<', '>', 'v'}, '╤': {'<', '>', 'v'},
        '┴': {'<', '>', '^'}, '╧': {'<', '>', '^'},
        '╥': {'<', '>', 'v'}, '╦': {'<', '>', 'v'},
        '╨': {'<', '>', '^'}, '╩': {'<', '>', '^'},
        '┼': {'^', 'v', '<', '>'},
        '╫': {'^', 'v', '<', '>'},
        '╪': {'^', 'v', '<', '>'},
    }
    ROTATION_MAP = {
        '┼': ('┼', 1), '╫': ('╪', 1), '╪': ('╫', 1), '╬': ('╬', 1),
        '─': ('│', 1), '│': ('─', 1), '═': ('║', 1), '║': ('═', 1),
        '┌': ('┐', 3), '┐': ('┘', 3), '┘': ('└', 3), '└': ('┌', 3),
        '╔': ('╗', 3), '╗': ('╝', 3), '╝': ('╚', 3), '╚': ('╔', 3),
        '├': ('┬', 3), '┬': ('┤', 3), '┤': ('┴', 3), '┴': ('├', 3),
        '╠': ('╦', 3), '╦': ('╣', 3), '╣': ('╩', 3), '╩': ('╠', 3),
        '╞': ('╥', 3), '╥': ('╡', 3), '╡': ('╨', 3), '╨': ('╞', 3),
        '╧': ('╟', 3), '╟': ('╤', 3), '╤': ('╢', 3), '╢': ('╧', 3),
        '╓': ('╖', 3), '╖': ('╜', 3), '╜': ('╙', 3), '╙': ('╓', 3),
        '╒': ('╕', 3), '╕': ('╛', 3), '╛': ('╘', 3), '╘': ('╒', 3),
    }

    def __init__(self, init_game):
        self.init_grid, (self.start, self.finish) = self.__parse_grid(init_game)
        self.grid_graph = self.__build_graph(self.init_grid)

    def __parse_grid(self, init_game):
        grid, start, finish = defaultdict(str), None, None
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

    def __print_screen(self, grid, control_type = None, pos=(0, 0)):

        def print_grid(grid, pos):
            bold_map = {
                '─': '━', '═': '━', '│': '┃', '║': '┃', ' ': '▮',
                '┌': '┏', '╔': '┏', '┐': '┓', '╗': '┓', '└': '┗',
                '╚': '┗', '┘': '┛', '╝': '┛', '┬': '┳', '╦': '┳',
                '╓': '┏', '╖': '┓', '╒': '┏', '╕': '┓',
                '╙': '┗', '╜': '┛', '╘': '┗', '╛': '┛',
                '╤': '┳', '╥': '┳', '┴': '┻', '╩': '┻', '╧': '┻',
                '╨': '┻', '├': '┣', '╠': '┣', '╞': '┣', '╟': '┣',
                '┼': '╋', '╬': '╋', '╪': '╋', '╫': '╋', '┤': '┫',
                '╣': '┫', '╡': '┫', '╢': '┫'
            }
            (min_r, min_c), (max_r, max_c) = min(grid), max(grid)
            grid_repl = copy.deepcopy(grid)
            grid_repl[pos] = bold_map.get(grid_repl[pos], '●')
            screen = [
                ''.join(str(grid_repl.get((r, c), ' '))
                for c in range(min_c, max_c + 1))
                for r in range(min_r, max_r + 1)
            ]
            return screen

        if control_type == "Numbers":
            num_cols = max(grid)[1] + 1
            full_screen = []
            first  = '   ' + ''.join(str(i // 10) for i in range(num_cols + 0))
            second = '   ' + ''.join(str(i % 10) for i in range(num_cols + 0))
            full_screen.extend([first, second])
            lines = print_grid(grid, pos)
            for i, line in enumerate(lines):
                print_line = f"{str(i).zfill(2)} {line} {str(i).zfill(2)}"
                full_screen.append(print_line)
            full_screen.extend([first, second])
            print('\n'.join(full_screen))
            print('_' * (len(full_screen[-1]) + 2))

        else:
            full_screen = print_grid(grid, pos)
            print('\n'.join(full_screen))
            print('_' * len(full_screen[-1]))

    def __rotate_pipe(self, pos, grid, rotations):

        current_char = grid[pos]
        new_char, mod = self.ROTATION_MAP.get(current_char, (current_char, 0))

        # Update rotation count and character
        rotations[pos] = (rotations.get(pos, 0) + 1) % (mod + 1)
        grid[pos] = new_char

        return rotations, grid

    def play_game(self, control_code = 3):
        """
        Control Key:
            1: "Numbers"
            2: "Arrows"
            3: "Auto"
        """
        control_type = self.REMOTE_CONTROL[control_code]

        grid = self.init_grid.copy()
        row, col = self.start
        max_r, max_c = self.finish[0] + 1, self.finish[1] + 1
        rotations_dict = defaultdict(int)
        key_hist = []

        if control_type == "Numbers":
            while True:
                self.__print_screen(grid, control_type, (row, col))
                print("Current Rotation Count:", sum(rotations_dict.values()))
                string = input('Enter (row, col) or "q" to QUIT: ')
                if string == 'q':
                    min_rots = sum(rotations_dict.values())
                    break
                try:
                    row, col = map(int, string.split(','))
                    col = max(col, self.start[0])
                    rotations_dict, grid = self.__rotate_pipe((row, col), grid, rotations_dict)
                except:
                    print('Invalid input. Try again.')

        elif control_type == "Arrows":
            while True:
                self.__print_screen(grid, control_type, (row, col))
                print("Current Rotation Count:", sum(rotations_dict.values()))
                click.echo('Use arrow keys or space to rotate, "q" to QUIT:')
                key = click.getchar()
                key_hist.append(key)
                if key == 'q':
                    min_rots = sum(rotations_dict.values())
                    # print(key_hist)
                    break
                elif key == '\xe0H': row = (row - 1) % max_r
                elif key == '\xe0P': row = (row + 1) % max_r
                elif key == '\xe0K': col = (col - 1) % max_c
                elif key == '\xe0M': col = (col + 1) % max_c
                elif key == ' ':  # space
                    rotations_dict, grid = self.__rotate_pipe((row, col), grid, rotations_dict)
                else:
                    print(f'Key {key} not recognized')

        elif control_type == "Auto":
            min_rots = self.auto_play(True)

        return min_rots

    def __build_graph(self, grid):
        graph = defaultdict(set)
        (min_r, min_c), (max_r, max_c) = self.start, self.finish
        for (r, c), val in grid.items():
            if not (min_r <= r <= max_r and min_c <= c <= max_c):
                continue
            if val not in self.VALID_SYMBOLS:
                continue
            for dir_sym, (dr, dc) in self.DIRECTIONS.items():
                nr, nc = r + dr, c + dc
                if (
                    min_r <= nr <= max_r and min_c <= nc <= max_c
                    and grid.get((nr, nc)) in self.VALID_SYMBOLS
                ):
                    graph[(r, c)].add((dir_sym, (nr, nc)))
        return graph

    def auto_play(self, visualization = False):
        grid = copy.deepcopy(self.init_grid)
        rotations = defaultdict(int)
        finalized = {self.finish, self.start}
        total_rotations = 0
        self.rots = 0

        def valid_rotations(pos):
            r, c = pos
            target_dirs = {pos for dir, pos in self.grid_graph[pos]}
            original = grid[pos]
            possible = []
            test_symbol = original
            possible_conns = self.PIPE_CONNECTIONS.get(test_symbol, set())
            for conn_dir in possible_conns:
                dr, dc = self.DIRECTIONS[conn_dir]
                nr, nc = r + dr, c + dc
                if (nr, nc) in target_dirs:
                    possible.append((nr, nc))
            return possible

        while True:
            progress = False
            if self.rots >= 10:
                break
            for pos in list(self.grid_graph.keys()):
                if pos in finalized:
                    continue
                options = valid_rotations(pos)
                for test_pos in options:
                    rotations, grid = self.__rotate_pipe(test_pos, grid, rotations)
                    if test_pos not in finalized:
                        total_rotations += 1
                        self.rots += 1
                    finalized.add(pos)
                progress = True

                # VISUALIZATION: print grid and rotation count after each finalized pipe
                if visualization:
                    print(f"Finalized pipe at {pos} with rotation(s). Total rotations: {total_rotations}")
                    self.__print_screen(grid, control_type=None, pos=pos)
                    time.sleep(0.5)  # half second delay to see the progress, adjust or remove as needed

            if not progress:
                break

        print("Auto-play complete. Total rotations:", total_rotations)
        return sum(rotations.values())

    def auto_play(self, visualization=False):
        from collections import defaultdict
        import copy, time

        grid = copy.deepcopy(self.init_grid)
        rotations = defaultdict(int)
        finalized = {self.start, self.finish}
        total_rotations = 0

        def valid_rotations(pos):
            r, c = pos
            original = grid[pos]
            possible = []
            neighbors = self.grid_graph[pos]

            test_symbol = original
            for rot in range(4):
                connections = self.PIPE_CONNECTIONS.get(test_symbol, set())
                ok = True

                for dir_name in connections:
                    dr, dc = self.DIRECTIONS[dir_name]
                    neighbor = (r + dr, c + dc)
                    neighbor_char = grid.get(neighbor)

                    if neighbor_char not in self.VALID_SYMBOLS:
                        ok = False
                        break

                    neighbor_conns = self.PIPE_CONNECTIONS.get(neighbor_char, set())

                    if neighbor in finalized:
                        # Neighbor is locked — must be compatible
                        if self.REVERSE_DIR[dir_name] not in neighbor_conns:
                            ok = False
                            break
                    else:
                        # Try all 4 rotations of neighbor to see if compatible
                        temp = neighbor_char
                        match_found = False
                        for _ in range(4):
                            temp_conns = self.PIPE_CONNECTIONS.get(temp, set())
                            if self.REVERSE_DIR[dir_name] in temp_conns:
                                match_found = True
                                break
                            temp, _ = self.ROTATION_MAP.get(temp, (temp, 0))
                        if not match_found:
                            ok = False
                            break

                if ok:
                    possible.append(rot)

                test_symbol, _ = self.ROTATION_MAP.get(test_symbol, (test_symbol, 0))

            return possible

        while True:
            progress = False
            for pos in list(self.grid_graph.keys()):
                if pos in finalized:
                    continue

                options = valid_rotations(pos)

                if len(options) == 1:
                    rot = options[0]
                    for _ in range(rot):
                        rotations, grid = self.__rotate_pipe(pos, grid, rotations)
                        total_rotations += 1
                    finalized.add(pos)
                    progress = True

                    if visualization:
                        print(f"Finalized pipe at {pos} with {rot} rotation(s). Total rotations: {total_rotations}")
                        self.__print_screen(grid, control_type=None, pos=pos)
                        time.sleep(0.5)

            if not progress:
                break

        print("Auto-play complete. Total rotations:", total_rotations)
        return sum(rotations.values())


pipes = PipesGame(input_data)

rotations = pipes.play_game(3)
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

