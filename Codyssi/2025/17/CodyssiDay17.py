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
D17_file = "Day17_input.txt"
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

    def __possible_steps(self, steps, valid_moves):
        step_paths = {}
        for step_idx, start_step in enumerate(steps):
            fwd_steps = steps[step_idx + 1:]
            for next_step in fwd_steps:
                step_len = next_step - start_step
                if step_len in valid_moves:
                    step_paths.setdefault(start_step, []).append(next_step)
        return step_paths

    def count_paths(self, possible_moves):
        start, end = self.step_info[0][1], self.step_info[0][2]
        all_steps = list(range(start, end + 1))
        step_dict = self.__possible_steps(all_steps, possible_moves)

        history = {}

        def dfs(current):
            if current == end: # If current is final step, count 1
                return 1
            if current in history: # If current is in history return to that point
                return history[current]
            total = 0
            for next_step in step_dict.get(current, []):
                total += dfs(next_step)
            history[current] = total
            return total

        return dfs(start)

stairs = Staircase(steps)

valid_paths = stairs.count_paths(possible_moves)
print("Part 1:", (valid_paths))

print(f"Execution Time = {time.time() - start_time:.5f}s")
