"""Challenge Code - Day 1, Year i18n
Solution Started: Mar 6, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/1/
Solution by: Abbas Moosajee
Brief: [Code/Problem Description]
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
print(input_data)
