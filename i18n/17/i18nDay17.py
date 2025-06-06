"""i18n Puzzles - Puzzle 17
Solution Started: Jun 2, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/17
Solution by: Abbas Moosajee
Brief: [X marks the spot]
"""

#!/usr/bin/env python3

import os, re, copy, time, binascii
from collections import defaultdict
from PIL import Image, ImageDraw, ImageFont
start_time = time.time()

# Load the input data from the specified file path
D17_file = "Day17_input.txt"
D17_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D17_file)

# Read and sort input data into a grid
with open(D17_file_path) as file:
    input_data = file.read().strip().split('\n\n')

import binascii
import os
from collections import defaultdict
from PIL import Image, ImageDraw, ImageFont

class ByteBeard:
    DIRECTIONS = {'>': (0, 1), 'v': (1, 0), '^': (-1, 0), '<': (0, -1)}
    BITS_IN_BYTES = 8

    def __init__(self, init_bytes):
        """Initialize ByteBeard with encoded puzzle pieces."""
        self.init_bytes = init_bytes
        self.puzzle_pieces = defaultdict(list)    # grid_no -> list of hex strings (lines)
        self.puzzle_sizes = defaultdict(int)      # grid_no -> number of lines
        self.puzzle_ids = {}                       # (grid_no, line_no) -> hex_string
        self.__build_puzzle_dict(init_bytes)

    @staticmethod
    def decode_map(map_section, visualize=True):
        """Decode a list of hex-encoded lines into UTF-8 strings."""
        decoded_map = []
        for line in map_section:
            try:
                byte_data = binascii.unhexlify(line)
                decoded_line = byte_data.decode('utf-8', errors='replace')
            except (binascii.Error, UnicodeDecodeError) as e:
                decoded_line = f"[Decode error: {e}]"
            decoded_map.append(decoded_line)

        if visualize:
            print('\n'.join(decoded_map))
        return decoded_map

    def create_hex_map(self, map_state, visualize=False):
        """Construct a hex string map from a mapping of positions to puzzle piece references."""
        (min_r, min_c), (max_r, max_c) = min(map_state), max(map_state)
        hex_map = []
        empty_hex = '20' * self.BITS_IN_BYTES  # space chars in hex

        for r in range(min_r, max_r + 1):
            row = ""
            for c in range(min_c, max_c + 1):
                pos = (r, c)
                grid_pos = map_state.get(pos, None)
                row += self.puzzle_ids.get(grid_pos, empty_hex)
            hex_map.append(row)

        if visualize:
            print('\n'.join(hex_map))
        return hex_map

    def print_map_grid(self, grid_map):
        """ Nicely print the map grid positions with formatting."""
        def format_cell(val):
            return f"({val[0]:03},{val[1]:02})" if val else "________"

        max_row = max(r for r, _ in grid_map)
        max_col = max(c for _, c in grid_map)

        for row in range(max_row + 1):
            line = [format_cell(grid_map.get((row, col))) for col in range(max_col + 1)]
            print(" ".join(line))

    def save_map(self, map_data, map_name="treasure_map", file_type="png"):
        """Save the decoded treasure map either as text or an image."""
        file_name = f"{map_name}.{file_type}"
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)

        if file_type == "txt":
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(map_data))
        else:
            font_path = "C:/Windows/Fonts/lucon.ttf"  # Adjust font path as needed
            font_size = 20
            font = ImageFont.truetype(font_path, font_size)

            dummy_img = Image.new("RGB", (1, 1))
            dummy_draw = ImageDraw.Draw(dummy_img)
            bbox = dummy_draw.textbbox((0, 0), "M", font=font)
            char_width, char_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

            rows, cols = self.map_props["H"], self.map_props["W"] * self.BITS_IN_BYTES
            img_width = char_width * cols
            img_height = char_height * rows

            image = Image.new("RGB", (img_width, img_height), "white")
            draw = ImageDraw.Draw(image)

            for y, line in enumerate(map_data):
                for x, ch in enumerate(line):
                    top_left = (x * char_width, y * char_height)
                    bottom_right = ((x + 1) * char_width, (y + 1) * char_height)
                    if ch == "╳":
                        draw.rectangle([top_left, bottom_right], fill="red")
                    else:
                        draw.text(top_left, ch, font=font, fill="black")

            image.save(file_path)

        print(f"{file_name} saved.")

    def __build_puzzle_dict(self, encoded_map):
        """Build dictionaries of puzzle pieces and their line hex strings."""
        for grid_no, section in enumerate(encoded_map):
            lines = section.split('\n')
            self.puzzle_pieces[grid_no] = lines
            self.puzzle_sizes[grid_no] = len(lines)
            for line_no, hex_line in enumerate(lines):
                self.puzzle_ids[(grid_no, line_no)] = hex_line

    def __identify_edges(self, map_grid):
        """Identify edges and corners in the puzzle map for placement logic."""
        edges_dict = defaultdict(list)
        map_size = defaultdict(int)

        CORNERS = {"╔": "T_L", "╗": "T_R", "╝": "B_R", "╚": "B_L"}
        EDGE_SETS = {"T": {"═", "-"}, "B": {"═", "-"}, "L": {"║", "|"}, "R": {"║", "|"}}
        CORNER_EDGES = {key: tuple(key.split('_')) for key in CORNERS.values()}

        for grid_no, section in map_grid.items():
            decoded = self.decode_map(section, visualize=False)
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
            raise ValueError("Edge lengths do not match.")

        w, h = map_size["B"] // self.BITS_IN_BYTES, map_size["R"]
        map_props = {
            "W": w, "H": h,
            "T_L": (0, 0), "T_R": (0, w - 1),
            "B_L": (h - 1, 0), "B_R": (h - 1, w - 1),
        }

        return edges_dict, map_props

    def __add_grid_to_map(self, grid_no, start_pos):
        """Place a puzzle grid at the specified starting position in the full map."""
        row, col = start_pos
        self.unused_grids.remove(grid_no)
        grid_len = self.puzzle_sizes[grid_no]
        for line_no in range(grid_len):
            self.full_map[(row + line_no, col)] = (grid_no, line_no)
            self.empty_spaces.remove((row + line_no, col))

    def __create_init_map(self, puzzle_pieces):
        """Initialize the map by placing corner grids."""
        self.edges_dict, self.map_props = self.__identify_edges(puzzle_pieces)
        self.full_map = {(r, c): None for r in range(self.map_props["H"]) for c in range(self.map_props["W"])}
        self.unused_grids = set(self.puzzle_sizes.keys())
        self.empty_spaces = set(self.full_map.keys())

        for corner in ["T_L", "T_R", "B_L", "B_R"]:
            row, col = self.map_props[corner]
            grid_no = self.edges_dict[corner]
            grid_len = self.puzzle_sizes[grid_no]
            # Adjust row for bottom corners
            if corner.startswith("B"):
                row = row - grid_len + 1
            self.__add_grid_to_map(grid_no, (row, col))

    @staticmethod
    def validate_utf8(hex_str, debug=False):
        """ Validate that a hex string represents valid UTF-8 bytes."""
        raw_bytes = binascii.unhexlify(hex_str)
        i = 0
        length = len(raw_bytes)

        while i < length:
            byte = raw_bytes[i]

            if byte >> 7 == 0b0:
                expected_len = 1
            elif byte >> 5 == 0b110:
                expected_len = 2
            elif byte >> 4 == 0b1110:
                expected_len = 3
            elif byte >> 3 == 0b11110:
                expected_len = 4
            elif byte >> 6 == 0b10:
                # Allow trailing continuation near the end
                if i >= length - 2:
                    if debug:
                        print(f"Allowing trailing continuation byte at pos {i}: {byte:#x}")
                    break
                if debug:
                    print(f"Unexpected standalone continuation byte at pos {i}: {byte:#x}")
                return False
            else:
                if debug:
                    print(f"Invalid leading byte at pos {i}: {byte:#x}")
                return False

            if i + expected_len > length:
                if debug:
                    print(f"Incomplete UTF-8 sequence at end starting at pos {i}")
                break

            # Validate continuation bytes
            for j in range(1, expected_len):
                cont_byte = raw_bytes[i + j]
                if cont_byte >> 6 != 0b10:
                    if debug:
                        print(f"Invalid continuation byte at pos {i + j}: {cont_byte:#x}")
                    return False

            i += expected_len

        if debug:
            print("UTF-8 validation passed.")
        return True

    def __identify_matches(self, map_pos, possible_grids):
        """ Find grids that can be placed at map_pos such that rows validate as UTF-8."""
        valid_grids = set()
        row, col = map_pos

        for grid_no in possible_grids:
            is_valid = True

            # Collect contiguous left neighbors
            left_neighbors = []
            c = col - 1
            while (cell := self.full_map.get((row, c))) is not None:
                left_neighbors.insert(0, cell)
                c -= 1

            # Collect contiguous right neighbors
            right_neighbors = []
            c = col + 1
            while (cell := self.full_map.get((row, c))) is not None:
                right_neighbors.append(cell)
                c += 1

            # Compose full row with candidate grid in the middle
            full_row = left_neighbors + [(grid_no, 0)] + right_neighbors
            min_lines = min(self.puzzle_sizes[g[0]] for g in full_row)

            for line_no in range(min_lines):
                combined_line = ""
                for g_no, g_row in full_row:
                    # For candidate grid, use line_no; for neighbors, adjust line index
                    grid_line = (g_row + line_no) if g_no != grid_no else line_no
                    hex_str = self.puzzle_ids.get((g_no, grid_line))
                    if hex_str is None:
                        break
                    combined_line += hex_str

                if not self.validate_utf8(combined_line, debug=False):
                    is_valid = False
                    break

            if is_valid:
                valid_grids.add(grid_no)

        return list(valid_grids)

    def __fill_the_map(self, remaining_grids, debug=False):
        """ Fill the map by placing grids where only one valid choice fits."""
        steps = 0
        grid_choices = remaining_grids.copy()
        empty_positions = self.empty_spaces.copy()

        while empty_positions and grid_choices:
            current_pos = min(empty_positions)
            matches = self.__identify_matches(current_pos, grid_choices)

            if len(matches) == 1:
                grid_to_place = matches[0]
                grid_choices.remove(grid_to_place)
                self.__add_grid_to_map(grid_to_place, current_pos)
                empty_positions = self.empty_spaces.copy()
            else:
                raise ValueError(f"More than one valid choice fits at {current_pos}: {matches}")
            steps += 1
            if steps >= len(self.puzzle_sizes):
                break

    def build_treasure_map(self, save_map=False):
        """Build the treasure map by arranging puzzle pieces and decoding."""
        self.__create_init_map(self.puzzle_pieces)
        remaining_grids = self.unused_grids.copy()
        self.__fill_the_map(remaining_grids, debug=False)

        hex_map = self.create_hex_map(self.full_map)
        treasure_map = self.decode_map(hex_map, visualize=False)
        if save_map:
            print('\n'.join(treasure_map))
            self.save_map(treasure_map)
        return treasure_map

    def find_treasure(self, treasure_map):
        """Find the coordinates of the treasure marker '╳' in the treasure map."""
        for y, row in enumerate(treasure_map):
            for x, ch in enumerate(row):
                if ch == "╳":
                    return {"x": x, "y": y}
        return {"x": 0, "y": 0}


beard = ByteBeard(input_data)
treasure_map = beard.build_treasure_map()

coord = beard.find_treasure(treasure_map)
print("X Coordinates:", coord["x"] * coord["y"])

# print(f"Execution Time = {time.time() - start_time:.5f}s")