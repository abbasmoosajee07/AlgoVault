"""Codyssi Puzzles - Problem 3
Solution Started: Apr 6, 2025
Puzzle Link: https://www.codyssi.com/view_problem_3?
Solution by: Abbas Moosajee
Brief: [Unformatted Readings]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D03_file = "Day03_input.txt"
D03_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D03_file)

# Read and sort input data into a grid
with open(D03_file_path) as file:
    input_data = file.read().strip().split('\n')
    input_data1 = "100011101111110010101101110011 2\n83546306 10\n1106744474 8\n170209FD 16\n2557172641 8\n2B290C15 16\n279222446 10\n6541027340 8".split('\n')
    map_readings = [(terrain, int(base)) for line in input_data for terrain, base in [line.split()]]

def to_base_65(n):
    symbols = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#"
    base = 65
    result = []

    while n > 0:
        remainder = n % base
        result.append(symbols[remainder])
        n //= base

    return ''.join(reversed(result))

base_sum, base10_sum = (0, 0)
for terrain, base in map_readings:
    base_sum += base
    base10_sum += int(terrain, base)

print("Part 1:", base_sum)
print("Part 2:", base10_sum)
print("Part 3:", to_base_65(base10_sum))  # Output: 30PzDC
