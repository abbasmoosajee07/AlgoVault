"""Codyssi Puzzles - Problem 11
Solution Started: Apr 12, 2025
Puzzle Link: https://www.codyssi.com/view_problem_15?
Solution by: Abbas Moosajee
Brief: [Games in a Storm]
"""

#!/usr/bin/env python3
import os, re, copy, math

# Load the input data from the specified file path
D11_file = "Day11_input.txt"
D11_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D11_file)

# Read and sort input data into a grid
with open(D11_file_path) as file:
    input_data = file.read().strip().split('\n')
    map_readings = [(terrain, int(base)) for line in input_data for terrain, base in [line.split()]]

SYMBOLS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^"

def from_base_n(s, base):
    value = 0
    for char in s:
        value = value * base + SYMBOLS.index(char)
    return value

def to_base_n(n, base):
    result = []
    while n > 0:
        result.append(SYMBOLS[n % base])
        n //= base
    return ''.join(reversed(result))

def find_max_base(x, max_digits):
    base_ceiling = math.floor((x + 1) ** (1 / max_digits))
    return base_ceiling + 1

file_numbers = []
for (terrain, base) in map_readings:
    if base > 36:
        base10_num = from_base_n(terrain, base)
    else:
        base10_num = int(terrain, base)
    file_numbers.append(base10_num)

file_sum = sum(file_numbers)
print("Part 1:", max(file_numbers))
print("Part 2:", to_base_n(file_sum, 68))
print("Part 3:", find_max_base(file_sum, 4))