"""Codyssi Puzzles - Problem 1
Solution Started: Apr 6, 2025
Puzzle Link: https://www.codyssi.com/view_problem_1?
Solution by: Abbas Moosajee
Brief: [Handling the Budget]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D01_file = "Day01_input.txt"
D01_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D01_file)

# Read and sort input data into a grid
with open(D01_file_path) as file:
    input_data = file.read().strip().split('\n')
    items_prices = list(map(int, input_data))

total_cost = sum(items_prices)
print("Part 1:", total_cost)

most_expensive_items = sorted(items_prices)[-20:]
print("Part 2:", total_cost - sum(most_expensive_items))

voucher_price = 0
for idx, num in enumerate(items_prices, start=1):
    if (idx % 2) == 0:
        voucher_price += num
    else:
        voucher_price -= num

print("Part 3:", abs(voucher_price))