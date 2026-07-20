"""FlipFlop 2026: BitFlop Internship - Puzzle 4
Solution Started: July 20, 2026
Puzzle Link: https://flipflop.slome.org/2026/4
Solution by: Abbas Moosajee
Brief: [Magic Flowerstalk]"""

#!/usr/bin/env python3
from pathlib import Path

# Load input file
input_file = "puzzle_04_input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()

def climb_plant(plant):
    swap_count = 0
    last_idx = 4
    for section in plant:
        leaf_idx = section.find("o")
        if leaf_idx != -1 and last_idx != leaf_idx:
            swap_count += 1
            last_idx = leaf_idx
    return swap_count

def count_workers(plant):
    workers = 0

    while any("o" in section for section in plant):
        workers += 1
        last_idx = 4
        last_section_idx = None

        for i, section in enumerate(plant):
            leaf_idx = section.find("o")
            if leaf_idx == -1:
                continue
            if leaf_idx != last_idx:
                if last_section_idx is not None:
                    plant[last_section_idx] = "  |  "
                last_idx = leaf_idx
            last_section_idx = i

        if last_section_idx is not None:
            plant[last_section_idx] = "  |  "
    return workers

print("FlipFlops 2026, Puzzle 04")
print("Part 1:", sum(1 for section in data[:-400] if "o" in section))
print("Part 2:", climb_plant(data[::-1]))
print("Part 3:", count_workers(data[::-1]))
