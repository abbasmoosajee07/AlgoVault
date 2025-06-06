"""i18n Puzzles - Puzzle 16
Solution Started: May 28, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/16
Solution by: Abbas Moosajee
Brief: [8-bit unboxing]
"""

#!/usr/bin/env python3

import os, re, copy, sys, time, click
from collections import defaultdict, deque, namedtuple
start_time = time.time()

# Load the input data from the specified file path
D16_file = "Day16_input.txt"
D16_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D16_file)

# Read and sort input data into a grid
with open(D16_file_path, encoding = "CP437") as file:
    input_data = file.read().strip().split('\n')

class PipesGame:
    REMOTE_CONTROL = {1: "Numbers", 2: "Arrows", 3: "Auto"}
    BoxChar = namedtuple("BoxChar", ["N", "E", "S", "W"])

    box_chars = {
        " ": BoxChar(0,0,0,0), "│": BoxChar(1,0,1,0), "┤": BoxChar(1,0,1,1),
        "╡": BoxChar(1,0,1,2), "╢": BoxChar(2,0,2,1), "╖": BoxChar(0,0,2,1),
        "╕": BoxChar(0,0,1,2), "╣": BoxChar(2,0,2,2), "║": BoxChar(2,0,2,0),
        "╗": BoxChar(0,0,2,2), "╝": BoxChar(2,0,0,2), "╜": BoxChar(2,0,0,1),
        "╛": BoxChar(1,0,0,2), "┐": BoxChar(0,0,1,1), "└": BoxChar(1,1,0,0),
        "┴": BoxChar(1,1,0,1), "┬": BoxChar(0,1,1,1), "├": BoxChar(1,1,1,0),
        "─": BoxChar(0,1,0,1), "┼": BoxChar(1,1,1,1), "╞": BoxChar(1,2,1,0),
        "╟": BoxChar(2,1,2,0), "╚": BoxChar(2,2,0,0), "╔": BoxChar(0,2,2,0),
        "╩": BoxChar(2,2,0,2), "╦": BoxChar(0,2,2,2), "╠": BoxChar(2,2,2,0),
        "═": BoxChar(0,2,0,2), "╬": BoxChar(2,2,2,2), "╧": BoxChar(1,2,0,2),
        "╨": BoxChar(2,1,0,1), "╤": BoxChar(0,2,1,2), "╥": BoxChar(0,1,2,1),
        "╙": BoxChar(2,1,0,0), "╘": BoxChar(1,2,0,0), "╒": BoxChar(0,2,1,0),
        "╓": BoxChar(0,1,2,0), "╫": BoxChar(2,1,2,1), "╪": BoxChar(1,2,1,2),
        "┘": BoxChar(1,0,0,1), "┌": BoxChar(0,1,1,0),
    }
    reverse_map = {v: k for k, v in box_chars.items()}

    @staticmethod
    def rotate_box_char_cw(c): return PipesGame.BoxChar(c.W, c.N, c.E, c.S)

    @staticmethod
    def has_single_orientation(c): return c == PipesGame.rotate_box_char_cw(c)

    @staticmethod
    def edge_counts(c): return set(c)

    @staticmethod
    def rotations(c):
        seen, r = set(), c
        for i in range(4):
            if r not in seen:
                yield i, r
                seen.add(r)
            r = PipesGame.rotate_box_char_cw(r)

    class EmptyCell:
        def __init__(self, char): self.char = char
        def __str__(self): return self.char
        def box_char(self): return PipesGame.BoxChar(0, 0, 0, 0)
        def is_locked(self): return True

    class PipeCell:
        def __init__(self, bc, locked=False):
            self._bc = bc
            self._locked = locked or PipesGame.has_single_orientation(bc)
        def __str__(self): return PipesGame.reverse_map[self._bc]
        def box_char(self): return self._bc
        def is_locked(self): return self._locked
        def rotate_cw(self, count=1):
            if self._locked: raise Exception("Can't rotate locked cell")
            for _ in range(count): self._bc = PipesGame.rotate_box_char_cw(self._bc)
            return count
        def lock(self): self._locked = True

    def __init__(self, input_data):
        self.base_grid, self.bounds = self.__parse_grid(input_data)

    def __parse_grid(self, data):
        grid, start, end = defaultdict(str), None, None
        start_mark, end_mark = "▐▐ Start ▌▌", "▐▐ Finish ▌▌"
        for r, line in enumerate(data):
            if start_mark in line: start = (r+1, line.index(start_mark) - 2)
            if end_mark in line: end = (r-1, line.index(end_mark) + len(end_mark) + 1)
            for c, ch in enumerate(line): grid[(r, c)] = ch
        return grid, ((start or min(grid)), (end or max(grid)))

    def __build_grid(self, dgrid):
        s, e = self.bounds
        g = {}
        for pos, ch in dgrid.items():
            if s <= pos <= e and ch in PipesGame.box_chars:
                g[pos] = self.PipeCell(PipesGame.box_chars[ch], pos in (s, e))
            else:
                g[pos] = self.EmptyCell(ch)
        return g

    def __get_cell(self, y, x):
        return self.cell_grid.get((y, x), self.EmptyCell(" "))

    def __valid_rotations(self, c, n, e, s, w):
        ns, es, ss, ws = map(PipesGame.edge_counts, \
            (n.box_char(), e.box_char(), s.box_char(), w.box_char()))
        if n.is_locked(): ns = {n.box_char().S}
        if e.is_locked(): es = {e.box_char().W}
        if s.is_locked(): ss = {s.box_char().N}
        if w.is_locked(): ws = {w.box_char().E}
        for count, rot in PipesGame.rotations(c.box_char()):
            if rot.N in ns and rot.E in es and rot.S in ss and rot.W in ws:
                yield count

    def __lock_pass(self):
        changed = 0
        for (y, x), cell in self.cell_grid.items():
            if isinstance(cell, self.PipeCell) and not cell.is_locked():
                options = list(self.__valid_rotations(
                    cell,
                    self.__get_cell(y-1, x), self.__get_cell(y, x+1),
                    self.__get_cell(y+1, x), self.__get_cell(y, x-1)))
                if len(options) == 1:
                    changed += cell.rotate_cw(options[0])
                    cell.lock()
                elif len(options) == 0:
                    cell.lock()
        return changed

    def __rotate_pipe(self, pos, grid, rotations):
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
        current_char = grid[pos]
        new_char, mod = ROTATION_MAP.get(current_char, (current_char, 0))

        # Update rotation count and character
        rotations[pos] = (rotations.get(pos, 0) + 1) % (mod + 1)
        grid[pos] = new_char

        return rotations, grid

    def print_screen(self, grid, control_type = None, pos = None):

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
            if pos is not None:
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

    def play_game(self, control_code = 3):
        """ 1: "Numbers" | 2: "Arrows"| 3: "Auto" """
        control_type = self.REMOTE_CONTROL[control_code]

        grid = self.base_grid.copy()
        start, finish = self.bounds
        row, col = start
        max_r, max_c = finish[0] + 1, finish[1] + 1
        rotations_dict = defaultdict(int)

        if control_type == "Numbers":
            while True:
                self.print_screen(grid, control_type, (row, col))
                print("Current Rotation Count:", sum(rotations_dict.values()))
                string = input('Enter (row, col) or "q" to QUIT: ')
                if string == 'q':
                    min_rots = sum(rotations_dict.values())
                    break
                try:
                    row, col = map(int, string.split(','))
                    col = max(col, start[0])
                    rotations_dict, grid = self.__rotate_pipe((row, col), grid, rotations_dict)
                except:
                    print('Invalid input. Try again.')
        elif control_type == "Arrows":
            while True:
                self.print_screen(grid, control_type, (row, col))
                print("Current Rotation Count:", sum(rotations_dict.values()))
                click.echo("\nUse WASD or arrow keys to move, space to rotate, enter to lock, 'q' to QUIT:")
                key = click.getchar()
                if key == 'q':
                    min_rots = sum(rotations_dict.values())
                    break
                elif key in ["w", "\xe0H"]: row = (row - 1) % max_r
                elif key in ["s", "\xe0P"]: row = (row + 1) % max_r
                elif key in ["a", "\xe0K"]: col = (col - 1) % max_c
                elif key in ["d", "\xe0M"]: col = (col + 1) % max_c
                elif key == ' ':  # space
                    rotations_dict, grid = self.__rotate_pipe((row, col), grid, rotations_dict)
                else:
                    print(f'Key {key} not recognized')
        elif control_type == "Auto":
            min_rots = 0
            self.cell_grid = self.__build_grid(grid)
            while (delta := self.__lock_pass()):
                min_rots += delta
            self.print_screen(self.cell_grid)

        return min_rots

game = PipesGame(input_data)
rotated = game.play_game(3)

print("Minimum Rotations Required:", rotated)

# print(f"Execution Time = {time.time() - start_time:.5f}s")
