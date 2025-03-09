"""i18n Puzzles - Puzzle 3
Solution Started: Mar 9, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/3/
Solution by: Abbas Moosajee
Brief: [Validating Passwords]
"""

#!/usr/bin/env python3

import os

# Load the input data from the specified file path
D03_file = "Day03_input.txt"
D03_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D03_file)

# Read and sort input data into a grid
with open(D03_file_path, encoding="utf-8") as file:
    input_data = file.read().strip().split('\n')

valid_passwords = [
    password for password in input_data
    if 4 <= len(password) <= 12             # Valid password length
    and any(c.isupper() for c in password)  # Has uppercase letter
    and any(c.islower() for c in password)  # Has lowercase letter
    and any(c.isdigit() for c in password)  # Has a digit
    and any(ord(c) > 127 for c in password)  # Contains non-ASCII character
]

print("No. of Valid Passwords:",len(valid_passwords))
