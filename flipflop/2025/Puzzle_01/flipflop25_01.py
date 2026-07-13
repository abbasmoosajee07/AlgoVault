"""FlipFlop Codes Puzzles - Puzzle 01
Solution Started: July 13, 2026
Puzzle Link: https://flipflop.slome.org/2025/1
Solution by: Abbas Moosajee
Brief: [Banana Contest]"""

#!/usr/bin/env python3
from pathlib import Path

# Load input file
input_file = "puzzle_01_input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    puzzle_data = f.read().splitlines()

def calculate_score(name_str):
    n = 2
    score = 0
    for i in range(0, len(name_str), n):
        if name_str[i:i+n] in ["ba", "na", "ne"]:
            score += 1
    return score

total_p1, total_p2, total_p3 = 0, 0, 0
for line_str in puzzle_data:
    line_score = calculate_score(line_str)
    total_p1 += line_score
    if line_score % 2 == 0:
        total_p2 += line_score
    if "ne" not in line_str:
        total_p3 += line_score

print("FlipFlop 25, Puzzle 01")
print("Part 1:", total_p1)
print("Part 2:", total_p2)
print("Part 3:", total_p3)
