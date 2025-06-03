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

    def __init__(self, init_bytes):
        self.rev_map_dict = defaultdict(bytes)    # (grid_no, line_no) -> hex_string
        self.map_dict = defaultdict(list)         # byte_data -> [(grid_no, line_no)]
        self.map_grid = {}                        # grid_no -> list of hex strings
        self.init_bytes = init_bytes
        self.__build_map_dict(init_bytes)

    def __build_map_dict(self, encoded_map):
        for grid_no, section in enumerate(encoded_map):
            lines = section.split('\n')
            self.map_grid[grid_no] = lines
            for line_no, hex_line in enumerate(lines):
                byte_data = bytes.fromhex(hex_line)
                self.map_dict[byte_data].append((grid_no, line_no))
                self.rev_map_dict[(grid_no, line_no)] = hex_line

    def decode_map(self, map_section, visualization = True):
        decoded_map = []
        for line in map_section:
            byte_data = bytes.fromhex(line)
            decoded_line = byte_data.decode('utf-8', errors='replace')
            decoded_map.append(decoded_line)
        if visualization:
            print('\n'.join(decoded_map))
        return decoded_map

    def identify_coordinates(self):
        # map_section = [
        #     "e295942de295902de295902de295902d",
        #     "7c7ee2898be2898bc3b1c3b1e2898b7e",
        #     "e29591c3b1c3b1e2898b7e7ee2898bf0",
        #     "7c7ec3b1c3b1f091808dc3b1e2898bf0"
        # ]
        # self.decode_map(map_section)
        # for line in map_section:
        #     byte_data = bytes.fromhex(line)
        #     decoded_line = byte_data.decode('utf-8', errors='replace')
        #     print(decoded_line, (str(byte_data)))
        return len(self.map_grid)

beard = ByteBeard(input_data)

coord = beard.identify_coordinates()
print("X Coordinates:", coord)

def is_start_of_utf8_char(byte):
    """Classify byte as start of multibyte UTF-8 character or continuation."""
    if byte >> 7 == 0b0:
        return 1  # 1-byte ASCII
    elif byte >> 5 == 0b110:
        return 2  # 2-byte sequence
    elif byte >> 4 == 0b1110:
        return 3  # 3-byte sequence
    elif byte >> 3 == 0b11110:
        return 4  # 4-byte sequence
    elif byte >> 6 == 0b10:
        return 0  # Continuation byte
    return -1     # Invalid byte

print(f"Execution Time = {time.time() - start_time:.5f}s")
