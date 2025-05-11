"""Codyssi Puzzles - Problem 17
Solution Started: May 10, 2025
Puzzle Link: https://www.codyssi.com/view_problem_21?
Solution by: Abbas Moosajee
Brief: [Spiralling Stairs]
"""

#!/usr/bin/env python3

import os, re, copy, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
start_time = time.time()

# Load the input data from the specified file path
D17_file = "Day17_input1.txt"
D17_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D17_file)

# Read and sort input data into a grid
with open(D17_file_path) as file:
    input_data = file.read().strip().split('\n\n')
    steps = input_data[0].split("\n")
    possible_moves = list(map(int, (input_data[1].split(":")[1]).strip().split(",")))

class Staircase:
    def __init__(self, steps):
        self.step_info = [self.parse_step(line) for line in steps]

    def parse_step(self, raw_info):
        info_list = raw_info.split()
        useful = (info_list[0], int(info_list[2]), int(info_list[4]),
                    info_list[7], info_list[9])
        return useful

    def count_paths(self, possible_moves):
        first, last = self.step_info[0], self.step_info[-1]
        print(first, last)
        return len(possible_moves)

stairs = Staircase(steps)

valid_paths = stairs.count_paths(possible_moves)
print("Part 1:", valid_paths)

print(f"Execution Time = {time.time() - start_time:.5f}s")
