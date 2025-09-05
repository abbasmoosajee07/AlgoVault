"""Eldarverse Puzzles - Problem D
Solution Started: September 4,
Puzzle Link: https://www.eldarverse.com/problem/sep-25-long-D
Solution by: Abbas Moosajee
Brief: [Code/Problem Description]"""

#!/usr/bin/env python3
from pathlib import Path

# Load input file
input_file = "problem-decryption-contest-1-D-input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()

print("Input Data:", data)


solutions = []
output_file = "problem-decryption-contest-1-D-output.txt"
output_path = Path(__file__).parent / output_file
with output_path.open("w", encoding="utf-8") as f:
    f.write("".join(solutions))