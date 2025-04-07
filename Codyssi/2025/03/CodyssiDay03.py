"""Codyssi Puzzles - Problem 3
Solution Started: Apr 7, 2025
Puzzle Link: https://www.codyssi.com/view_problem_7?
Solution by: Abbas Moosajee
Brief: [Supplies in Surplus]
"""

#!/usr/bin/env python3

import os

# Load the input data from the specified file path
D03_file = "Day03_input.txt"
D03_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D03_file)

# Read and sort input data into a grid
with open(D03_file_path) as file:
    input_data = file.read().strip().split('\n')

count_p1, count_p2, pile_sets = (0, 0, [])

for line in input_data:
    line_box = set()
    for box_range in line.split():
        min_box, max_box = map(int, box_range.split('-'))
        count_p1 += (max_box - min_box) + 1
        box_sets = set(range(min_box, max_box + 1))
        line_box.update(box_sets)

    count_p2 += len(line_box)
    pile_sets.append(line_box)

max_adjacent = 0
for i in range(len(pile_sets) - 1):
    combined = pile_sets[i] | pile_sets[i + 1]
    max_adjacent = max(max_adjacent, len(combined))

print("Part 1:", count_p1)
print("Part 2:", count_p2)
print("Part 3:", max_adjacent)
