"""i18n Puzzles - Puzzle 17
Solution Started: Jun 2, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/17
Solution by: Abbas Moosajee
Brief: [X marks the spot]
"""

#!/usr/bin/env python3

import os, re, copy, time
from collections import defaultdict
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
start_time = time.time()

# Load the input data from the specified file path
D17_file = "Day17_input1.txt"
D17_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D17_file)

# Read and sort input data into a grid
with open(D17_file_path) as file:
    input_data = file.read().strip().split('\n\n')

class ByteBeard:
    BITS_IN_BYTES = 8
    SYMBOLS = "├─┬┴┼┤│║╠╦╪╬╣╞╤╩╡╟╥╢╓╫╖╚═╝╙╨╜╘╧╛└┘╒╕┌┐╔╗"

    def __init__(self, init_bytes):
        self.init_bytes = init_bytes
        self.rev_map_dict = defaultdict(str)      # (grid_no, line_no) -> hex_string
        self.map_dict = defaultdict(list)         # byte_data -> [(grid_no, line_no)]
        self.map_grid = {}                        # grid_no -> list of hex strings
        self.__build_map_dict(init_bytes)
        self.treasure_map = self.build_map()

    def __reverse_dict(self, original):
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

    def create_hex_map(self, map_state, visualization=True):
        (min_r, min_c), (max_r, max_c) = min(map_state), max(map_state)
        printed_map = []
        for r in range(min_r, max_r + 1):
            row = ""
            for c in range(min_c, max_c + 1):
                pos = (r, c)
                grid_pos = map_state.get(pos, None)
                row += self.rev_map_dict.get(grid_pos, '20' * self.BITS_IN_BYTES)
            printed_map.append(row)
        if visualization:
            print('\n'.join(printed_map))
        return printed_map

    def __build_map_dict(self, encoded_map):
        for grid_no, section in enumerate(encoded_map):
            lines = section.split('\n')
            self.map_grid[grid_no] = lines
            for line_no, hex_line in enumerate(lines):
                byte_data = bytes.fromhex(hex_line)
                self.map_dict[byte_data].append((grid_no, line_no))
                self.rev_map_dict[(grid_no, line_no)] = hex_line

    def __identify_edges(self):
        edges_dict = defaultdict(list)
        map_size = defaultdict(int)

        CORNERS = {"╔": "T_L", "╗": "T_R", "╝": "B_R", "╚": "B_L"}
        EDGE_SETS = {"T": {"═", "-"}, "B": {"═", "-"}, "L": {"║", "|"}, "R": {"║", "|"}}
        CORNER_EDGES = {key: tuple(key.split('_')) for key in CORNERS.values()}

        for grid_no, section in self.map_grid.items():
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

    def __build_init_map(self):
        self.edges_dict, self.map_props = self.__identify_edges()
        self.rev_edges = self.__reverse_dict(self.edges_dict)
        self.unused_grids = set(self.map_grid.keys())
        full_map = {(row, col): None
            for row in range(self.map_props["H"])
            for col in range(self.map_props["W"])
        }
        for corner in ["T_L", "T_R", "B_L", "B_R"]:
            row_no, col_no = self.map_props[corner]
            grid_no = self.edges_dict[corner]
            grid_len = len(self.map_grid[grid_no])
            self.unused_grids.remove(grid_no)

            row_no = row_no if corner[0] == "T" else (row_no - grid_len)
            for line_no in range(grid_len):
                full_map[(row_no, col_no)] = (grid_no, line_no)
                row_no += 1
        return full_map

    @staticmethod
    def is_continuation_byte(b):
        return 0x80 <= b <= 0xBF

    @staticmethod
    def expected_length(first_byte):
        if 0xC2 <= first_byte <= 0xDF:
            return 2
        elif 0xE0 <= first_byte <= 0xEF:
            return 3
        elif 0xF0 <= first_byte <= 0xF4:
            return 4
        else:
            return 0

    def extract_incomplete_utf8(self, data: bytes) -> bytes:
        i = len(data)
        while i > 0:
            try:
                data[:i].decode('utf-8')
                break
            except UnicodeDecodeError:
                i -= 1
        return data[i:]

    def find_valid_completions(self, incomplete_byte, valid_sections):
        byte_val = incomplete_byte[0]
        seq_len = self.expected_length(byte_val)
        if seq_len == 0:
            return []

        needed = seq_len - 1
        candidates = []

        for data, positions in self.map_dict.items():
            for pos in positions:
                if pos[0] not in valid_sections:
                    continue
                for i in range(len(data) - needed):
                    cont_bytes = data[i:i + needed]
                    if all(self.is_continuation_byte(b) for b in cont_bytes):
                        full_seq = bytes([byte_val] + list(cont_bytes))
                        try:
                            full_seq.decode("utf-8")
                            candidates.append(pos)
                        except UnicodeDecodeError:
                            continue
        return candidates

    def __find_matches(self, grid_no, valid_sections=None):
        valid_sections = range(len(self.map_grid)) if valid_sections is None else valid_sections
        grid_hex = self.map_grid[grid_no]
        grid_matches = []
        for line_no, line in enumerate(grid_hex):
            byte_data = bytes.fromhex(line)
            rem_bytes = self.extract_incomplete_utf8(byte_data)
            if rem_bytes:
                matches = self.find_valid_completions(rem_bytes, valid_sections)
                grid_matches.extend(((grid_no, line_no), m) for m in matches)
        return grid_matches

    def __create_row(self, row_name):
        pos_grids = [self.edges_dict[side] for side in [f"{row_name}_R", f"{row_name}_L"]]
        pos_grids.extend(self.edges_dict[row_name])
        start_grid = self.edges_dict[f"{row_name}_L"]
        possible_matches = self.__find_matches(start_grid, pos_grids)
        return

    def add_grid_to_map(self, full_map, grid_no, start_pos):
        row_no, col_no = start_pos
        grid_len = len(self.map_grid[grid_no])

        for line_no in range(grid_len):
            full_map[(row_no, col_no)] = (grid_no, line_no)
            row_no += 1
        return full_map

    def build_map(self):
        full_map = self.__build_init_map()
        edge_secs = [item for x in self.edges_dict.values() for item in (x if isinstance(x, list) else [x])]
        mid_grids = list(self.map_grid.keys() - (edge_secs))
        full_map = self.add_grid_to_map(full_map, 0, (0, 1))
        formed_map = self.create_hex_map(full_map, False)
        self.decode_map(formed_map)
        # print(len(self.unused_grids))
        # for edge in "TBRL":
        #     print(edge, self.edges_dict[edge])
        return full_map

    def find_coordinates(self):

        return len(self.map_grid)

beard = ByteBeard(input_data)

coord = beard.find_coordinates()
print("X Coordinates:", coord)

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