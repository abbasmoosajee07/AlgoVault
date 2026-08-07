"""FlipFlop 2026: BitFlop Internship - Puzzle 11
Solution Started: August 3, 2026
Puzzle Link: https://flipflop.slome.org/2026/11
Solution by: Abbas Moosajee
Brief: [Humongous Trees]"""

#!/usr/bin/env python3
from pathlib import Path
from collections import defaultdict, deque

# Load input file
input_file = "puzzle_11_input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().split("\n\n")

data1 = ['    02          XX          00\n01  00  XX  01  01  02  XX  02  XX']

class HumongousTrees:

    DIRECTIONS = {"L": (0, -1), "R": (0, 1), "T": (1, 0)}
    ROOT_ID = "00"
    def __init__(self, raw_dna):
        self.raw_dna = raw_dna
        self.dna_dict = self.parse_dna(raw_dna)

    @staticmethod
    def parse_dna(raw_dna):
        def split_row(row: str, chunk_len: int = 10, gap: int = 2):
            step = chunk_len + gap
            return [row[i:i + chunk_len].split("  ") for i in range(0, len(row), step)]
        parsed = {}
        test = {}
        for line_no, block in enumerate(raw_dna):
            bottom_row, top_row = block.split("\n")[::-1][:2]
            bottom_chunks = split_row(bottom_row)
            top_chunks = split_row(top_row)
            for stem, (bottom, top) in enumerate(zip(bottom_chunks, top_chunks)):
                parsed_stem = bottom[1]
                if stem != int(parsed_stem):
                    raise ValueError(
                        f"Parsing error on line {line_no}: expected stem {stem}, got {parsed_stem}"
                    )
                parsed[(line_no, parsed_stem)] = {
                    "L": bottom[0],
                    "R": bottom[2],
                    "T": top[2],
                }
        return parsed

    @staticmethod
    def parse_dna1(raw_dna):

        def split_row(row: str, chunk_len: int = 10, gap: int = 2):
            step = chunk_len + gap
            return [row[i:i + chunk_len].split("  ") for i in range(0, len(row), step)]

        dna_dict = {}
        for line_no, block in enumerate(raw_dna):
            bottom_row, top_row = block.split("\n")[::-1][:2]
            bottom_chunks = split_row(bottom_row)
            top_chunks = split_row(top_row)
            for stem, (bottom, top) in enumerate(zip(bottom_chunks, top_chunks)):
                dna_id = bottom[1]
                parsed_stem = int(dna_id)
                if stem != parsed_stem:
                    raise ValueError(
                        f"Parsing error on line {line_no}: expected stem {stem}, got {parsed_stem}"
                    )
                dna_dict[dna_id] = {
                    "L": bottom[0],
                    "R": bottom[2],
                    "T": top[2],
                }
        return dna_dict

    def build_tree(self, num_years, visualize=False):
        sprouts = {(1, 0): (0, self.ROOT_ID)}
        stems = set()

        if visualize:
            self._render(sprouts, stems)

        for _year in range(num_years):
            candidates = defaultdict(list)  # coord -> list of (dna_id, line_no) candidates
            for (height, col), (line_no, dna_id) in sprouts.items():
                growth = self.dna_dict[(line_no, dna_id)]
                stems.add((height, col))  # always becomes a stem this year

                for direction, new_id in growth.items():
                    if new_id == "XX":
                        continue
                    dh, dc = self.DIRECTIONS[direction]
                    new_coord = (height + dh, col + dc)
                    if new_coord in stems:
                        continue  # blocked: a stem already permanently occupies this cell
                    candidates[new_coord].append((new_id, line_no))

            new_sprouts = {}
            for coord, entries in candidates.items():

                winner_id, winner_line = max(entries, key=lambda e: int(e[0]))
                new_sprouts[coord] = (winner_line, winner_id)

            sprouts = new_sprouts

            if visualize:
                self._render(sprouts, stems)

        return {"sprouts": sprouts, "stems": stems}

    @staticmethod
    def _render(sprouts, stems):
        all_coords = list(sprouts) + list(stems)
        if not all_coords:
            return
        max_height = max(h for h, _ in all_coords)
        min_col = min(c for _, c in all_coords) - 1
        max_col = max(c for _, c in all_coords) + 1

        for height in range(max_height, 0, -1):
            row = []
            for col in range(min_col, max_col + 1):
                if (height, col) in sprouts:
                    row.append("@")
                elif (height, col) in stems:
                    row.append("#")
                else:
                    row.append(".")
            print(f"{height:02d}:{''.join(row)}")
        print()

trees = HumongousTrees(data1)
print("FlipFlop 2026, Puzzle 10")
print("Part 1:", trees.build_tree(5, True))