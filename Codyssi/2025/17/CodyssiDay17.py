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
    def __init__(self, steps, possible_moves):
        self.staircase_data = {data[0]: data for line in steps for data in [self.parse_step(line)]}
        self.valid_moves = possible_moves

    def parse_step(self, raw_info):
        info_list = raw_info.split()
        useful = (info_list[0], int(info_list[2]), int(info_list[4]),
                    info_list[7], info_list[9])
        return useful

    def dfs(self, current, end, structure, history):
        if current == end: # If current is final step, count 1
            return 1
        if current in history: # If current is in history return to that point
            return history[current]
        total = 0
        for next_step in structure.get(current, []):
            total += self.dfs(next_step, end, structure, history)
        history[current] = total
        return total

    def single_stair_paths(self, target_step):

        start, end = self.staircase_data[target_step][1], self.staircase_data[target_step][2]
        all_steps = list(range(start, end + 1))
        step_dict = {}
        for step_idx, start_step in enumerate(all_steps):
            fwd_steps = all_steps[step_idx + 1:]
            for next_step in fwd_steps:
                step_len = next_step - start_step
                if step_len in self.valid_moves:
                    step_dict.setdefault(start_step, []).append(next_step)

        return self.dfs(start, end, step_dict, {})

    def __build_staircase(self, structure, stair_info):
        """ `S{X} : {N1} -> {N2} : FROM S{A} TO S{B}` """
        S_X, N1, N2, S_A, S_B = stair_info

        sx_start, sx_end = f"{S_X}_{N1}",  f"{S_X}_{N2}"
        branch_point, return_point = f"{S_A}_{N1}",  f"{S_B}_{N2}"
        if S_A != "START" or S_B != "END":
            structure.setdefault(branch_point, []).append(sx_start)
            structure.setdefault(sx_end, []).append(return_point)

        avail_steps = list(range(N1, N2 + 1))
        for step_idx, start_step in enumerate(avail_steps):
            fwd_steps = avail_steps[step_idx + 1:]
            for next_step in fwd_steps:
                structure.setdefault(f"{S_X}_{start_step}", []).append(f"{S_X}_{next_step}")

        return structure

    def multiple_stair_paths(self):
        stair_structure = {}
        for branch in self.staircase_data.values():
            stair_structure = self.__build_staircase(stair_structure, branch)

        # for step_part in stair_structure.items():
        #     print(step_part)

        count = self.dfs("S1_0", "S1_6", stair_structure, {})
        return count

stairs = Staircase(steps, possible_moves)

single_stair = stairs.single_stair_paths("S1")
print("Part 1:", single_stair)

multiple_stairs = stairs.multiple_stair_paths()
print("Part 2:", multiple_stairs)

print(f"Execution Time = {time.time() - start_time:.5f}s")

# S1_0-S1_1-S1_2-S1_3-S1_4-S1_5-S1_6
# S1_0-S1_1-S1_2-S1_3-S1_6
# S1_0-S1_1-S1_2-S1_5-S1_6
# S1_0-S1_1-S1_2-S2_2-S1_4-S1_5-S1_6
# S1_0-S1_1-S1_2-S2_2-S2_3-S1_3-S1_4-S1_5-S1_6
# S1_0-S1_1-S1_2-S2_2-S2_3-S1_3-S1_6
# S1_0-S1_1-S1_2-S2_2-S2_3-S1_5-S1_6
# S1_0-S1_1-S1_4-S1_5-S1_6
# S1_0-S1_1-S2_3-S1_3-S1_4-S1_5-S1_6
# S1_0-S1_1-S2_3-S1_3-S1_6
# S1_0-S1_1-S2_3-S1_5-S1_6
# S1_0-S1_3-S1_4-S1_5-S1_6
# S1_0-S1_3-S1_6
# S1_0-S2_2-S1_4-S1_5-S1_6
# S1_0-S2_2-S2_3-S1_3-S1_4-S1_5-S1_6
# S1_0-S2_2-S2_3-S1_3-S1_6
# S1_0-S2_2-S2_3-S1_5-S1_6