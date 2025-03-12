"""i18n Puzzles - Puzzle 5
Solution Started: Mar 11, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/5/
Solution by: Abbas Moosajee
Brief: [Don't step in it...]
"""

#!/usr/bin/env python3

import os

# Load the input data from the specified file path
D05_file = "Day05_input.txt"
D05_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D05_file)

# Read and sort input data into a grid
with open(D05_file_path, encoding="utf-8") as file:
    input_data = file.read().split('\n')

# Define grid dimensions
WIDTH, HEIGHT = len(input_data[0]), len(input_data)

# Create a dictionary representing the grid
grid = {(r, c): cell for r, row in enumerate(input_data) for c, cell in enumerate(row)}


# Initialize variables
shit_count = 0
row, col = 0, 0

# Traverse the grid
while row < HEIGHT:
    row += 1
    col = (col + 2) % WIDTH
    if grid.get((row, col)) == "💩":
        shit_count += 1

print("Stepped in shit:", shit_count)
