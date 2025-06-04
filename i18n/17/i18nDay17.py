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
            byte_data = bytes.fromhex(line)
            decoded_line = byte_data.decode('utf-8', errors=error_handling)
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
        width, height = (map_size["B"] // self.BITS_IN_BYTES), map_size["R"]
        map_props = {}
        map_props["W"], map_props["H"] = width, height
        map_props["T_L"], map_props["T_R"] = (0, 0), (0, width - 1)
        map_props["B_L"], map_props["B_R"] = (height, 0), (height, width - 1)
        return edges_dict, map_props

    def __add_grid_to_map(self, grid_no, start_pos):
        row_no, col_no = start_pos
        grid_len = self.puzzle_sizes[grid_no]

        for line_no in range(grid_len):
            self.full_map[(row_no, col_no)] = (grid_no, line_no)
            row_no += 1
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
        for corner in ["T_L", "T_R", "B_L", "B_R"]:
            row_no, col_no = self.map_props[corner]
            grid_no = self.edges_dict[corner]
            grid_len = self.puzzle_sizes[grid_no]

            row_no = row_no if corner[0] == "T" else (row_no - grid_len)
            self.full_map = self.__add_grid_to_map(grid_no, (row_no, col_no))

        return self.full_map

    def find_coordinates(self):
        position = {"x": 0, "y": 0}
        treasure_map = self.build_map()
        treasure_map = []
        for row_no, row_data in enumerate(treasure_map):
            for col_no, cell in enumerate(row_data):
                if cell == "╳":
                    position = {"x":col_no, "y":row_no}
        return position

    ## Solving the Puzzle -----------------------------------------------------
    @staticmethod
    def find_complete_utf8(hex_str: str, debug: bool = False) -> bool:
        # Convert hex string to raw bytes
        raw_bytes = binascii.unhexlify(hex_str)
        length = len(raw_bytes)
        i = 0

        while i < length:
            byte = raw_bytes[i]

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

            # If the sequence doesn't fit in remaining bytes
            if i + expected > length:
                # Allow if this is the final sequence
                if i == length - 1 or i == length - 2 or i == length - 3:
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

    def build_line(self, line_history, new_grid, line_no):
        return ''.join(self.puzzle_dict[(grid, line_no)] for grid in line_history + [new_grid])

    def __validate_matches(self, line_history, possible_choices):
        valid_grids = set()
        adj_grid = line_history[-1]
        adj_grid_len = self.puzzle_sizes[adj_grid]

        for possible_grid in possible_choices:
            possible_grid_len = self.puzzle_sizes[possible_grid]
            chosen_len = min(adj_grid_len, possible_grid_len)
            valid_choice = True
            for line_no in range(chosen_len):
                new_line = ""
                for line_pos in line_history:
                    new_line += self.puzzle_dict[(line_pos, line_no)]

                new_line += self.puzzle_dict[(possible_grid, line_no)]

                validity_check = self.find_complete_utf8(new_line)
                if not validity_check:
                    valid_choice = False
                    break
            if valid_choice:
                valid_grids.add(possible_grid)

        return list(valid_grids)

    def __complete_top_bottom(self, vertice_name):
        possible_grids = self.edges_dict[vertice_name]
        chosen_grid = self.edges_dict[f"{vertice_name}_L"]
        map_pos = self.map_props[f"{vertice_name}_L"]
        end_row = self.map_props[f"{vertice_name}_R"]
        count = 0
        line_history = [chosen_grid]
        while True:
            new_map_pos = map_pos[0], map_pos[1] + 1
            if new_map_pos == end_row:
                break
            count += 1
            selected_grids = self.__validate_matches(line_history, possible_grids)
            if len(selected_grids) == 1:
                chosen_grid = selected_grids[0]
                self.__add_grid_to_map(chosen_grid, new_map_pos)
                line_history.append(chosen_grid)
                possible_grids.remove(chosen_grid)
                map_pos = new_map_pos
            if count >= 8:
                break
        return selected_grids

    def build_map(self, print_map = True):
        self.full_map = self.__build_init_map()
        print(set(self.puzzle_sizes.values()))

        # puzzle_moves = [(0, (0, 1)), (3, (4, 1)), (2, (8, 2)), (6, (16, 1))]
        # puzzle_moves = []
        # for grid_no, edge_pos in puzzle_moves:
        #     self.full_map = self.__add_grid_to_map(grid_no, edge_pos)

        top_row = self.__complete_top_bottom("T")
        # bottom_row = self.__create_row("B")
        edge_secs = [item for x in self.edges_dict.values() for item in (x if isinstance(x, list) else [x])]
        mid_grids = list(self.puzzle_pieces.keys() - (edge_secs))
        formed_map = self.create_hex_map(self.full_map, False)
        treasure_map = self.decode_map(formed_map, True)

        print("Unused grids", len(self.unused_grids))
        print("Full Map Size:", len(self.full_map))
        # for edge in "TBRL":
        #     print(edge, self.edges_dict[edge])
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
