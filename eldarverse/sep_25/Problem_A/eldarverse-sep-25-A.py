"""Eldarverse Puzzles - Problem A
Solution Started: September 4,
Puzzle Link: https://www.eldarverse.com/problem/sep-25-long-B
Solution by: Abbas Moosajee
Brief: [Your name, Your Discount]"""


#!/usr/bin/env python3
from pathlib import Path

# Load input file
input_file = "problem-sep-25-long-A-input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()

solutions = []

for name_no, name in enumerate(data[1:], start=1):
    letter_counter = set()
    for letter in name:
        letter_counter.add(letter.lower())
    total_discount = len(letter_counter) * 5
    new_price = max(100 - total_discount, 0)
    solutions.append(f"Case #{name_no}: {new_price}")
    print(solutions[-1])

output_file = "problem-sep-25-long-A-output.txt"
output_path = Path(__file__).parent / output_file
with output_path.open("w", encoding="utf-8") as f:
    f.write("\n".join(solutions) + "\n")
