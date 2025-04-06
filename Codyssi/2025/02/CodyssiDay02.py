"""Codyssi Puzzles - Problem 2
Solution Started: Apr 6, 2025
Puzzle Link: https://www.codyssi.com/view_problem_6?
Solution by: Abbas Moosajee
Brief: [Absurd Arithmetic]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statistics import median

# Load the input data from the specified file path
D02_file = "Day02_input.txt"
D02_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D02_file)

# Read and sort input data into a grid
with open(D02_file_path) as file:
    input_data = file.read().strip().split('\n\n')
    room_qualities = list(map(int, input_data[1].splitlines()))
    pricing_functions = input_data[0].splitlines()

from statistics import median
import operator

# Preprocess the pricing steps once into callable operations
def parse_function(step):
    if 'ADD' in step:
        return lambda x, v=int(step.split('ADD')[1]): x + v
    elif 'MULTIPLY' in step:
        return lambda x, v=int(step.split('MULTIPLY')[1]): x * v
    elif 'RAISE TO THE POWER OF' in step:
        return lambda x, v=int(step.split('RAISE TO THE POWER OF')[1]): x ** v

# Create list of function objects in reverse order
parsed_steps = [parse_function(step) for step in pricing_functions[::-1]]

# Efficient pricing function using pre-parsed steps
def price_functions(num: int):
    for fn in parsed_steps:
        num = fn(num)
    return num

# Part 1
median_quality = median(room_qualities)
print("Part 1:", price_functions(median_quality))

# Part 2
even_quality_sum = sum(q for q in room_qualities if q % 2 == 0)
print("Part 2:", price_functions(even_quality_sum))

# Part 3
# Only call price_functions once per value
valid_prices = [(q, price_functions(q)) for q in room_qualities]
valid_rooms = [q for q, p in valid_prices if p <= 15_000_000_000_000]
print("Part 3:", max(valid_rooms))
