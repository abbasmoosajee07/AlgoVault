"""FlipFlop Codes Puzzles - Puzzle 00
Solution Started: July 13, 2026
Puzzle Link: https://flipflop.slome.org/2025/demo
Solution by: Abbas Moosajee
Brief: [Grandma's lost password]"""

#!/usr/bin/env python3
from pathlib import Path
from collections import Counter
# Load input file
input_file = "puzzle_00_input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()

num_data = [int(num) for num in data]

def count_digits(num_data):
    digit_str = ""
    for num_int in num_data:
        digit_str += str(num_int)
    return Counter(digit_str)

print("FlipFlop Demo Puzzle")
print("Part 1:", sum(num_data))
print("Part 2:", round(sum(num_data) / len(num_data)))
print(f"Part 3: {Counter(num_data).most_common()[0][0]}{count_digits(num_data).most_common()[-1][0]}")

