"""Codyssi Puzzles - Problem 8
Solution Started: Apr 10, 2025
Puzzle Link: https://www.codyssi.com/view_problem_12?
Solution by: Abbas Moosajee
Brief: [Risky Shortcut]
"""

#!/usr/bin/env python3

import os

# Load the input data from the specified file path
D08_file = "Day08_input.txt"
D08_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D08_file)

# Read and sort input data into a grid
with open(D08_file_path) as file:
    input_data = file.read().strip().split('\n')

alphabet_count = [letter for letter in ''.join(input_data) if letter.isalpha()]
print("Part 1:", len(alphabet_count))

def complete_reduction(base_string: str, consider_hyphen: bool = True) -> int:
    hyphen_check = '-' if consider_hyphen else ''

    def can_reduce_pair(c1, c2, hyphen):
        return (c1.isdigit() and (c2.isalpha() or c2 == hyphen)) or \
                (c2.isdigit() and (c1.isalpha() or c1 == hyphen))

    s = list(base_string)

    while True:
        reduced = False
        i = 0
        while i < len(s) - 1:
            if can_reduce_pair(s[i], s[i+1], hyphen_check):
                # Remove both s[i] and s[i+1]
                del s[i:i+2]
                reduced = True
                break  # Start over from beginning
            i += 1
        if not reduced:
            break

    return len(s)

reduced_file_p2 = [complete_reduction(line) for line in input_data]
print("Part 2:", sum(reduced_file_p2))

reduced_file_p3 = [complete_reduction(line, False) for line in input_data]
print("Part 2:", sum(reduced_file_p3))