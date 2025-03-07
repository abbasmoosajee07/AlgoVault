"""i18n Puzzles - Puzzle 1
Solution Started: Mar 7, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/1/
Solution by: Abbas Moosajee
Brief: [Message Length Limits]
"""

#!/usr/bin/env python3

import os, re, copy

# Load the input data from the specified file path
D01_file = "Day01_input.txt"
D01_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D01_file)

# Read and sort input data into a grid
with open(D01_file_path, encoding="utf-8") as file:
    input_data = file.read().strip().split("\n")

MESSAGE_COSTS = {"NONE": 0, "TWEET": 7, "SMS": 11, "BOTH": 13}

total_cost = 0

for message in input_data:
    characters = len(message)
    bytes_size = len(message.encode("utf-8"))

    if characters <= 140 and bytes_size <= 160:
        message_type = "BOTH"
    elif characters <= 140:
        message_type = "TWEET"
    elif bytes_size <= 160:
        message_type = "SMS"
    else:
        message_type = "NONE"

    cost = MESSAGE_COSTS[message_type]
    total_cost += cost

    # Debugging (optional)
    # print(f"{characters=}, {bytes_size=}, {message_type=}, {cost=}, {total_cost=}")

print("Total Cost:", total_cost)