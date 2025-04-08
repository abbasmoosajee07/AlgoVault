"""Codyssi Puzzles - Problem 6
Solution Started: Apr 8, 2025
Puzzle Link: https://www.codyssi.com/view_problem_10?
Solution by: Abbas Moosajee
Brief: [Lotus Scramble]
"""

#!/usr/bin/env python3

import os, re, copy, string
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D06_file = "Day06_input.txt"
D06_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D06_file)

# Read and sort input data into a grid
with open(D06_file_path) as file:
    input_data = file.read()

LETTER_DICTS = {letter: idx for idx, letter in enumerate(string.ascii_letters, start=1)}

uncorrupted_data = []
data_value = []

for char in input_data:
    if char.isalpha():
        char_value = LETTER_DICTS[char]
        data_value.append(char_value)
        uncorrupted_data.append(char_value)
    else:
        corrupt_value = (char_value * 2) - 5

        # Adjust corrupt_value to be within the range [1, 52]
        while corrupt_value < 1:
            corrupt_value += 52
        while corrupt_value > 52:
            corrupt_value -= 52

        if 1 <= corrupt_value <= 52:
            data_value.append(corrupt_value)
            char_value = corrupt_value

print("Part 1:", len(uncorrupted_data))
print("Part 2:", sum(uncorrupted_data))
print("Part 3:", sum(data_value))
