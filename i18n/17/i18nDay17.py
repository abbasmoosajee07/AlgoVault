"""i18n Puzzles - Puzzle 17
Solution Started: Jun 2, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/17
Solution by: Abbas Moosajee
Brief: [X marks the spot]
"""

#!/usr/bin/env python3

import os, re, copy, time, binascii
from collections import defaultdict
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
start_time = time.time()

# Load the input data from the specified file path
D17_file = "Day17_input.txt"
D17_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D17_file)

# Read and sort input data into a grid
with open(D17_file_path) as file:
    input_data = file.read().strip().split('\n\n')

class ByteBeard:
    DIRECTIONS = {'>': (0, 1), 'v': (1, 0), '^': (-1, 0), '<': (0, -1)}
    EDGE_MOVE = {"T":(">", "v"), "B":(">", "^"), "R":("v", "<"), "L":("v", ">")}
    BITS_IN_BYTES = 8
    SYMBOLS = "├─┬┴┼┤│║╠╦╪╬╣╞╤╩╡╟╥╢╓╫╖╚═╝╙╨╜╘╧╛└┘╒╕┌┐╔╗"

    def __init__(self, init_bytes):
        self.init_bytes = init_bytes
        self.puzzle_bytes = defaultdict(list)     # byte_data -> [(grid_no, line_no)]
        self.puzzle_dict = defaultdict(str)       # (grid_no, line_no) -> hex_string
        self.puzzle_pieces = defaultdict(list)    # grid_no -> list of hex strings
        self.puzzle_sizes = defaultdict(int)      # grid_no -> grid_size
        self.__build_puzzle_dict(init_bytes)

    @staticmethod
    def __reverse_dict(original):
        reversed_dict = defaultdict(str)
        for k, v in original.items():
            if isinstance(v, list):
                for item in v:
                    reversed_dict[item] = k
            else:
                reversed_dict[v] = k
        return reversed_dict

    def decode_map(self, map_section, visualization=True, error_handling='replace'):
        decoded_map = []
        for line in map_section:
            try:
                byte_data = binascii.unhexlify(line)
                decoded_line = byte_data.decode('utf-8', errors=error_handling)
            except (binascii.Error, UnicodeDecodeError) as e:
                decoded_line = f"[Decode error: {e}]"
            decoded_map.append(decoded_line)

        if visualization:
            print('\n'.join(decoded_map))
        return decoded_map

    def create_hex_map(self, map_state, visualization = False):
        (min_r, min_c), (max_r, max_c) = min(map_state), max(map_state)
        printed_map = []
        for r in range(min_r, max_r + 1):
            row = ""
            for c in range(min_c, max_c + 1):
                pos = (r, c)
                grid_pos = map_state.get(pos, None)
                row += self.puzzle_dict.get(grid_pos, '20' * self.BITS_IN_BYTES)
            printed_map.append(row)
        if visualization:
            print('\n'.join(printed_map))
        return printed_map

    def print_map_grid(self):
        grid_map = self.full_map
        # Determine grid dimensions
        def format_cell(val):
            if val is None:
                return "________"
            return f"({val[0]:03},{val[1]:02})"

        # Grid dimensions
        max_row = max(r for r, _ in grid_map)
        max_col = max(c for _, c in grid_map)

        # Print the grid
        for row in range(max_row + 1):
            line = []
            for col in range(max_col + 1):
                cell = format_cell(grid_map.get((row, col)))
                line.append(cell)
            print(" ".join(line))

    def __build_puzzle_dict(self, encoded_map):
        for grid_no, section in enumerate(encoded_map):
            lines = section.split('\n')
            self.puzzle_pieces[grid_no] = lines
            self.puzzle_sizes[grid_no] = len(lines)

            for line_no, hex_line in enumerate(lines):
                byte_data = bytes.fromhex(hex_line)
                self.puzzle_bytes[byte_data].append((grid_no, line_no))
                self.puzzle_dict[(grid_no, line_no)] = hex_line

    def __identify_edges(self, map_grid):
        edges_dict = defaultdict(list)
        map_size = defaultdict(int)

        CORNERS = {"╔": "T_L", "╗": "T_R", "╝": "B_R", "╚": "B_L"}
        EDGE_SETS = {"T": {"═", "-"}, "B": {"═", "-"}, "L": {"║", "|"}, "R": {"║", "|"}}
        CORNER_EDGES = {key: tuple(key.split('_')) for key in CORNERS.values()}

        for grid_no, section in map_grid.items():
            decoded = self.decode_map(section, False)
            if not decoded:
                continue

            top, bottom = decoded[0], decoded[-1]
            left_edge = [line[0] for line in decoded if line]
            right_edge = [line[-1] for line in decoded if line]
            EDGE_SLICES = {"T": top, "B": bottom, "L": left_edge, "R": right_edge}

            for edge, valid_chars in EDGE_SETS.items():
                if set(EDGE_SLICES[edge]).issubset(valid_chars):
                    edges_dict[edge].append(grid_no)
                    map_size[edge] += len(EDGE_SLICES[edge])

            chars = set(''.join(decoded))
            for corner, label in CORNERS.items():
                if corner in chars:
                    edges_dict[label] = grid_no
                    for edge in CORNER_EDGES[label]:
                        map_size[edge] += len(EDGE_SLICES[edge])
                    break

        if map_size["T"] != map_size["B"] or map_size["R"] != map_size["L"]:
            raise ValueError("Edge Lengths do not match.")
        w, h = (map_size["B"] // self.BITS_IN_BYTES), map_size["R"]
        map_props = {
            "W": w, "H": h,
            "T_L": (0, 0), "T_R": (0, w - 1),
            "B_L": (h - 1, 0), "B_R": (h - 1, w - 1),
        }

        return edges_dict, map_props

    def __add_grid_to_map(self, grid_no, start_pos):
        row_no, col_no = start_pos
        grid_len = self.puzzle_sizes[grid_no]
        self.piece_edges[grid_no]["S"] = (row_no, col_no)
        for line_no in range(grid_len):
            self.full_map[(row_no, col_no)] = (grid_no, line_no)
            self.empty_spaces.remove((row_no, col_no))
            row_no += 1
        self.piece_edges[grid_no]["E"] = (row_no -1, col_no)
        self.unused_grids.remove(grid_no)
        return self.full_map

    def __build_init_map(self):
        self.edges_dict, self.map_props = self.__identify_edges(self.puzzle_pieces)
        self.rev_edges = self.__reverse_dict(self.edges_dict)
        self.unused_grids = set(self.puzzle_pieces.keys())
        self.full_map = {(row, col): None
            for row in range(self.map_props["H"])
            for col in range(self.map_props["W"])
        }
        self.empty_spaces = copy.deepcopy(set(self.full_map.keys()))
        self.piece_edges = defaultdict(dict)
        for corner in ["T_L", "T_R", "B_L", "B_R"]:
            row_no, col_no = self.map_props[corner]
            grid_no = self.edges_dict[corner]
            grid_len = self.puzzle_sizes[grid_no]

            row_no = row_no if corner[0] == "T" else (row_no - grid_len + 1)
            self.full_map = self.__add_grid_to_map(grid_no, (row_no, col_no))

        return self.full_map

    def find_coordinates(self):
        position = {"x": 0, "y": 0}
        treasure_map = self.build_map()
        # treasure_map = []
        for row_no, row_data in enumerate(treasure_map):
            for col_no, cell in enumerate(row_data):
                if cell == "╳":
                    position = {"x":col_no, "y":row_no}
        # print("Unused grids", len(self.unused_grids), "| Full Map Size:", len(self.full_map))
        return position

    ## Solving the Puzzle -----------------------------------------------------
    @staticmethod
    def __find_complete_utf8(hex_str: str, debug: bool = False) -> bool:
        raw_bytes = binascii.unhexlify(hex_str)

        length = len(raw_bytes)
        i = 0

        while i < length:
            byte = raw_bytes[i]

            # Check for continuation byte in first position (allowed if at start)
            if byte >> 6 == 0b10:
                if i == 0:
                    # Skip initial dangling continuation byte
                    i += 1
                    continue
                else:
                    if debug:
                        print(f"Unexpected continuation byte at position {i}: {byte:#x}")
                    return False

            # Determine expected length of UTF-8 sequence
            if byte >> 7 == 0b0:
                expected = 1
            elif byte >> 5 == 0b110:
                expected = 2
            elif byte >> 4 == 0b1110:
                expected = 3
            elif byte >> 3 == 0b11110:
                expected = 4
            else:
                if debug:
                    print(f"Invalid UTF-8 leading byte at position {i}: {byte:#x}")
                return False

            # If sequence doesn't fully fit and it's not at end, it's invalid
            if i + expected > length:
                if i == 0 or i + expected - 1 >= length:
                    # Incomplete sequence is allowed at start or end
                    break
                else:
                    if debug:
                        print(f"Incomplete UTF-8 sequence in middle at byte {i}: {raw_bytes[i:].hex()}")
                    return False

            # Check continuation bytes
            for j in range(1, expected):
                cont = raw_bytes[i + j]
                if cont >> 6 != 0b10:
                    if debug:
                        print(f"Invalid continuation byte at position {i + j}: {cont:#x}")
                    return False

            i += expected

        if debug:
            print("No incomplete UTF-8 sequences in the middle.")
        return True

    def __validate_matches(self, map_pos, possible_choices, block_moves=(">", "v"), debug=False, start_grid=None):
        valid_grids = set()
        row, col = map_pos
        count_upward = block_moves[1] == "^"

        for test_grid_no in possible_choices:
            test_grid_len = self.puzzle_sizes[test_grid_no]
            is_valid = True

            if debug:
                print(f"\nTesting grid {test_grid_no} at position {map_pos} (upward: {count_upward})")

            # Collect left neighbors
            left_cells = []
            c = col - 1
            while (cell := self.full_map.get((row, c))) is not None:
                left_cells.insert(0, cell)
                c -= 1

            # Collect right neighbors
            right_cells = []
            c = col + 1
            while (cell := self.full_map.get((row, c))) is not None:
                right_cells.append(cell)
                c += 1

            # Determine starting row index for the test grid
            grid_row = start_grid if start_grid is not None else (test_grid_len - 1 if count_upward else row)
            full_row = left_cells + [(test_grid_no, grid_row)] + right_cells

            if debug:
                print("→ Full row layout:", full_row)

            min_lines = min(self.puzzle_sizes[g[0]] for g in full_row)

            for line_no in range(min_lines):
                row_chars = []
                row_coords = []
                for g_no, g_row in full_row:
                    g_len = self.puzzle_sizes[g_no]
                    if count_upward:
                        g_line = g_len - line_no - 1
                    elif start_grid is not None:
                        g_line = (g_row + line_no) if g_no != test_grid_no else line_no
                    else:
                        g_line = g_row + line_no
                    pos = (g_no, g_line)

                    row_coords.append(pos)
                    row_chars.append(self.puzzle_dict[pos])

                row_chars = [self.puzzle_dict[pos] for pos in row_coords]

                combined_line = ''.join(row_chars)

                if debug:
                    self.decode_map([combined_line])

                if not self.__find_complete_utf8(combined_line):
                    is_valid = False
                    break
            if is_valid:
                valid_grids.add(test_grid_no)

        return list(valid_grids)

    def __complete_vertices(self, label, axis="horizontal", debug=False):
        pieces_remaining = self.edges_dict[label]
        movement = self.EDGE_MOVE[label]
        direction = self.DIRECTIONS[movement[0]]
        if axis == "vertical":
            top_piece = self.edges_dict[f"T_{label}"]
            current_pos = self.piece_edges[top_piece]["E"]
            target_pos = self.map_props[f"B_{label}"]
            max_steps = 10
        elif axis == "horizontal":
            current_pos = self.map_props[f"{label}_L"]
            target_pos = self.map_props[f"{label}_R"]
            max_steps = 50  # safety limit
        steps = 0
        while current_pos != target_pos and steps < max_steps:
            next_pos = tuple(c + d for c, d in zip(current_pos, direction))
            match_options = self.__validate_matches(
                next_pos, pieces_remaining,  block_moves=movement,
                debug=debug if axis != "horizontal" else False,
                start_grid=0 if axis != "horizontal" else None
            )
            if len(match_options) == 1:
                g = match_options[0]
                if axis == "horizontal":
                    # For vertical chains, adjust offset for bottom pieces
                    offset = (next_pos[0] - self.puzzle_sizes[g] + 1, next_pos[1]) \
                            if g in self.edges_dict["B"] else next_pos
                else:
                    offset = next_pos
                self.__add_grid_to_map(g, offset)
                pieces_remaining.remove(g)
                if axis == "vertical":
                    current_pos = self.piece_edges[g]["E"]
                else:
                    current_pos = next_pos
            else:
                break
            steps += 1

    def __complete_map(self, rem_grids, debug=False):
        steps = 0
        grid_choices = rem_grids.copy()
        empty_positions = self.empty_spaces.copy()
        while True:
            init_pos = min(empty_positions)
            # print(steps, init_pos)
            match_options = self.__validate_matches(init_pos, grid_choices, debug = debug, start_grid=0)
            # print(init_pos, match_options)
            # if len(match_options) != 1:
            #     print(init_pos, match_options)
            #     print(len(grid_choices), len(empty_positions))
            if len(match_options) == 1:
                g = match_options[0]
                self.__add_grid_to_map(g, init_pos)
                empty_positions = self.empty_spaces.copy()
                grid_choices = self.unused_grids.copy()
                # print(match_options, len(grid_choices), len(empty_positions))
            else:
                break
            steps += 1
            if steps >= 50:
                break
            if len(grid_choices) == 0:
                break
        return
    def build_map(self, print_map = True):
        self.full_map = self.__build_init_map()
        # print(f"Puzzle Sizes: {set(self.puzzle_sizes.values())}|Left Edge: {self.edges_dict["L"]}|Right Edge: {self.edges_dict["R"]}")
        self.EDGES_MAP = copy.deepcopy(self.edges_dict)

        self.__complete_vertices("T", axis="horizontal")
        self.__complete_vertices("B", axis="horizontal")
        self.__complete_vertices("L", axis="vertical")
        # right_edge = [(62, (8, 31)), (132, (32, 31)), (25, (48, 31)), (27, (72, 31))]
        # # right_edge = [(62, (8, 31)), (132, (56, 31)), (25, (32, 31)), (27, (72, 31))]
        # puzzle_moves = right_edge
        # for grid_no, edge_pos in puzzle_moves:
        #     self.full_map = self.__add_grid_to_map(grid_no, edge_pos)
        # self.__complete_vertices("R", axis="vertical")
        rem_grids = copy.deepcopy(self.unused_grids)
        self.__complete_map(rem_grids, False)

        formed_map = self.create_hex_map(self.full_map)
        treasure_map = self.decode_map(formed_map, False)

        # self.print_map_grid()
        # for line in treasure_map:
        #     print(line)
        return treasure_map

beard = ByteBeard(input_data)

coord = beard.find_coordinates()
print("X Coordinates:", coord["x"] * coord["y"])

print(f"Execution Time = {time.time() - start_time:.5f}s")

# ╔-═-═-═-═-═-═-═--═-═-═-╗
# |~≋≋ññ≋~~ñ𑀍≋ñ~~ñ≋~ññ𑀍~ñ|
# ║ññ≋~~≋𑀍~≋~ññ~ñ~ñññ≋ñ~~║
# |~ññ𑀍ñ≋𑀍-¯~ñññññññ−-¯¯ñ|
# ║~≋ñ~¯-𐲣-¯¯¯ñ~≋𑀍≋ñ----ñ║
# |ñ≋ññ−-𐲣-¯¯-ñññ𑀍ñ¯¯−¯-~|
# ║ñ≋~~¯−𐲣--¯¯-~ñ𑀍≋~¯--ññ║
# |~≋ññ𐲣-−¯¤¯−-≋~≋~ñ≋¯≋~~|
# ║~~ññ~𐲣𐲣¯¯𐲣---ññ~ñ~~≋ññ║
# |~ñ≋𑀍~≋≋--¯¯¯≋ñ~~𑀍~≋ñ~≋|
# ║ñ≋ñññ~𑀍ñ~¯ññ~~𑀍~~~ñ~≋ñ║
# |ññ≋~≋ñ≋~≋-ñ╳~≋≋-−-¯−~ñ|
# ║ñ~ññññ≋~ññ≋𑀍~~𑀍--¯-¯-ñ║
# |≋ñ~≋ñ≋~ññ~𑀍ñ~≋𑀍¯¯¯−--~|
# ║~~𑀍~~ñ≋≋-ñ≋~ñ~𐲣•.¤-−-~║
# |ñ≋ññññ𑀍-¯~-¯≋−𐳓:¤..¯¯≋|
# ║~ñ𑀍≋~~¯¯−-𐲣--¤𐳓¨¨¤.--~║
# |~ññ≋≋-𐲣--𐲣-¯𐲣.𐳓¤..−¯-ñ|
# ║≋~ñ𑀍--𐲣−-−--¯-𐳓.¤¤.¯-~║
# |≋ñ≋¯¯¯¯-𐲣-¯¯-¯−¯¯-−¯-≋|
# ║ñ≋-¯¯-−-ñ¯~≋~≋≋--¯¯¯¯ñ║
# |≋ñ¯¯¯≋≋≋~~~𑀍ñ~ñ≋~≋~ñ-≋|
# ║ñ~~~𑀍~≋ñ~~≋ññ≋≋ñññ~≋~~║
# ╚-═-═-═-═-═-═-═--═-═-═-╝

