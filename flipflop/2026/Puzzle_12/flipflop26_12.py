"""FlipFlop 2026: BitFlop Internship - Puzzle 12
Solution Started: August 10, 2026
Puzzle Link: https://flipflop.slome.org/2026/12
Solution by: Abbas Moosajee
Brief: [Bingo Bango Bongo]"""

#!/usr/bin/env python3
from pathlib import Path
from collections import defaultdict

# Load input file
input_file = "puzzle_12_input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().split("\n\n")

class FlipFlopBingo:
    def __init__(self, bingo_cards):
        self.bingo_cards = bingo_cards

    @staticmethod
    def _check_bingos(marked_cards, valid_bingos):
        bingo_count = 0
        for marks in marked_cards.values():
            for possible_bingo in valid_bingos:
                if set(possible_bingo) <= marks:
                    bingo_count += 1
        return bingo_count

    def play_bingo(self, calls, bingo_type = "2d"):
        if bingo_type == "4d":
            val_pos = self.parse_4d_cards(self.bingo_cards)
            valid_bingos = self._find_4d_bingos(5, 5, 5, 5)
        elif bingo_type == "3d":
            val_pos = self._parse_3d_cards(self.bingo_cards)
            valid_bingos = self._find_3d_bingos(5, 5, 5)
        else:
            val_pos = self._parse_2d_cards(self.bingo_cards)
            valid_bingos = self._find_2d_bingos(5, 5)

        marked_cards = defaultdict(set)
        for val in calls.split():
            for card_no, coord in val_pos[int(val)]:
                marked_cards[card_no].add(coord)
            if self._check_bingos(marked_cards, valid_bingos) >= 5:
                return val
        return -1

    @staticmethod
    def _parse_2d_cards(bingo_cards):
        val_pos = defaultdict(list)
        for card_no, card_data in enumerate(bingo_cards.split("\n")):
            numbers = [int(n) for n in card_data.split()]
            rows = [numbers[i:i + 5] for i in range(0, len(numbers), 5)]
            for row_no, row_data in enumerate(rows):
                for col_no, val in enumerate(row_data):
                    val_pos[int(val)].append((card_no, (row_no, col_no)))
        return val_pos

    @staticmethod
    def _find_2d_bingos(total_rows, total_cols):
        rows = [[(row_no, col_no) for col_no in range(total_cols)] for row_no in range(total_rows)]
        cols = [[(row_no, col_no) for row_no in range(total_rows)] for col_no in range(total_cols)]
        diagonals = []
        if total_rows == total_cols:
            n = total_rows
            diagonals.append([(i, i) for i in range(n)])
            diagonals.append([(i, n - 1 - i) for i in range(n)])
        return rows + cols + diagonals

    @staticmethod
    def _parse_3d_cards(bingo_cards):
        val_pos = defaultdict(list)
        grids = []
        for line in bingo_cards.split("\n"):
            numbers = [int(n) for n in line.split()]
            rows = [numbers[i:i + 5] for i in range(0, len(numbers), 5)]
            grids.append(rows)
        cubes = [grids[i:i + 5] for i in range(0, len(grids), 5)]

        for cube_no, cube in enumerate(cubes):
            for depth, grid in enumerate(cube):
                for row_no, row in enumerate(grid):
                    for col_no, val in enumerate(row):
                        val_pos[val].append((cube_no,( row_no, col_no, depth)))
        return val_pos

    @staticmethod
    def _find_3d_bingos(total_rows, total_cols, total_depth, line_len=5):
        dirs = [
            (dx, dy, dz)
            for dx in (-1, 0, 1) for dy in (-1, 0, 1) for dz in (-1, 0, 1)
            if (dx, dy, dz) != (0, 0, 0)
        ]
        lines = set()
        for x in range(total_rows):
            for y in range(total_cols):
                for z in range(total_depth):
                    for dx, dy, dz in dirs:
                        cells = [(x + dx*i, y + dy*i, z + dz*i) for i in range(line_len)]
                        if all(0 <= cx < total_rows and 0 <= cy < total_cols and 0 <= cz < total_depth
                            for cx, cy, cz in cells):
                            lines.add(frozenset(cells))
        return [sorted(line) for line in lines]

    @staticmethod
    def parse_4d_cards(bingo_cards):
        val_pos = defaultdict(list)
        grids = []
        for line in bingo_cards.split("\n"):
            numbers = [int(n) for n in line.split()]
            rows = [numbers[i:i + 5] for i in range(0, len(numbers), 5)]
            grids.append(rows)

        cubes = [grids[i:i + 5] for i in range(0, len(grids), 5)]
        hypercubes = [cubes[i:i + 5] for i in range(0, len(cubes), 5)]

        for hc_no, hypercube in enumerate(hypercubes):
            for w, cube in enumerate(hypercube):
                for depth, grid in enumerate(cube):
                    for row_no, row in enumerate(grid):
                        for col_no, val in enumerate(row):
                            val_pos[val].append((hc_no, (row_no, col_no, depth, w)))
        return val_pos

    @staticmethod
    def _find_4d_bingos(total_rows, total_cols, total_depth, total_trice, line_len=5):
        dirs = [
            (dx, dy, dz, dw)
            for dx in (-1, 0, 1)
            for dy in (-1, 0, 1)
            for dz in (-1, 0, 1)
            for dw in (-1, 0, 1)
            if (dx, dy, dz, dw) != (0, 0, 0, 0)
        ]
        lines = set()
        for x in range(total_rows):
            for y in range(total_cols):
                for z in range(total_depth):
                    for w in range(total_trice):
                        for dx, dy, dz, dw in dirs:
                            cells = [
                                (x + dx*i, y + dy*i, z + dz*i, w + dw*i)
                                for i in range(line_len)
                            ]
                            if all(
                                0 <= cx < total_rows and 0 <= cy < total_cols
                                and 0 <= cz < total_depth and 0 <= cw < total_trice
                                for cx, cy, cz, cw in cells
                            ):
                                lines.add(frozenset(cells))
        return [sorted(line) for line in lines]

flip_bingo = FlipFlopBingo(data[1])

print("FlipFlop 2026, Puzzle 12")
print("Part 1:", flip_bingo.play_bingo(data[0], "2d"))
print("Part 2:", flip_bingo.play_bingo(data[0], "3d"))
print("Part 3:", flip_bingo.play_bingo(data[0], "4d"))
