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

class HumongousTrees:

    DIRECTIONS = {"L": (0, -1), "R": (0, 1), "T": (1, 0)}

    def __init__(self, raw_dna):
        self.raw_dna = raw_dna
        self.dna_dict = self.parse_dna(raw_dna)

    @staticmethod
    def parse_dna(raw_dna):
        def split_row(row: str, chunk_len: int = 10, gap: int = 2):
            step = chunk_len + gap
            return [row[i:i + chunk_len].split("  ") for i in range(0, len(row), step)]
        parsed = {}
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

    def receivable_energy(self, stems):
        by_col = defaultdict(list)
        for height, col in stems:
            by_col[col].append(height)

        total_energy = 0
        for col, heights in by_col.items():
            heights.sort()
            n = len(heights)
            for idx, height in enumerate(heights):
                blocking = n - 1 - idx  # count of taller stems in this column
                multiplier = max(0, 3 - blocking)
                total_energy += min(height, 10) * multiplier
        return total_energy

    def _grow_tree(self, stems, sprouts):
        stems.update(sprouts.keys())

        candidates = defaultdict(list)  # coord -> list of dna_id candidates
        for (height, col), (dna_line, dna_id) in sprouts.items():
            growth = self.dna_dict[(dna_line, dna_id)]

            for direction, new_id in growth.items():
                if new_id == "XX":
                    continue
                dh, dc = self.DIRECTIONS[direction]
                new_coord = (height + dh, col + dc)
                if new_coord in stems:
                    continue  # blocked: a stem already permanently occupies this cell
                candidates[new_coord].append((dna_line, new_id))

        new_sprouts = {}
        for coord, entries in candidates.items():
            winner_id = max(entries, key=lambda e: int(e[1]))
            new_sprouts[coord] = winner_id
        return stems, new_sprouts

    def build_single_tree(self, dna_group, num_years=100, visualize=False):
        sprouts = {(1, 0): (dna_group, "00")}
        stems = set()

        if visualize:
            self._render(sprouts, stems)
        for year in range(1, num_years + 1):
            stems, sprouts = self._grow_tree(stems, sprouts)
            if visualize:
                self._render(sprouts, stems)

            avail_biomass = len(sprouts) + len(stems)
            energy_reqd = avail_biomass * 3
            energy_avail = self.receivable_energy(stems)

            if (year >= 5 and energy_avail < energy_reqd):
                break
        return avail_biomass

tree = HumongousTrees(data)

biomass_p1 = [tree.build_single_tree(dna_line) for dna_line in range(len(tree.raw_dna))]

print("FlipFlop 2026, Puzzle 11")
print("Part 1:", sum(biomass_p1))
