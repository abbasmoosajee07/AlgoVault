"""Codyssi Puzzles - Problem 12
Solution Started: Apr 13, 2025
Puzzle Link: https://www.codyssi.com/view_problem_16?
Solution by: Abbas Moosajee
Brief: [Challenging the Whirlpool]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D12_file = "Day12_input.txt"
D12_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D12_file)

# Read and sort input data into a grid
with open(D12_file_path) as file:
    input_data = file.read().strip().split('\n\n')
    num_grid = [list(map(int, line.split(' '))) for line in input_data[0].split('\n')]
    instructions = input_data[1].split('\n')
    control_actions = input_data[2].split('\n')

class CharybdisWhirlpool:
    def __init__(self, grid: list[list[int]], instructions: list[str]):
        self.grid_array = np.array(grid)
        self.instructions = instructions

    @staticmethod
    def rotate_list(nums, k):
        k = k % len(nums)  # normalize k
        rotated = np.concatenate((nums[-k:], nums[:-k]))  # concatenate arrays
        return rotated

    @staticmethod
    def calculate_property_sum(grid: list[list[int]], sum_prop: str = "max"):
        if sum_prop == "max":
            return  max(np.sum(grid, axis=num).max() for num in [0, 1])
        elif sum_prop == "min":
            return  min(np.sum(grid, axis=num).min() for num in [0, 1])

    def perform_instructions(self, instructions, num_grid):
        grid_array = np.array(num_grid.copy())
        for command in instructions:
            cmd_list = command.split()
            op = cmd_list[0]

            if op == "SHIFT":
                shift_idx = int(cmd_list[2]) - 1
                shift_val = int(cmd_list[-1])
                axis = cmd_list[1]

                if axis == "COL":
                    grid_array[:, shift_idx] = self.rotate_list(grid_array[:, shift_idx], shift_val)
                elif axis == "ROW":
                    grid_array[shift_idx] = self.rotate_list(grid_array[shift_idx], shift_val)

            elif op in {"ADD", "SUB", "MULTIPLY"}:
                value = int(cmd_list[1])
                axis = cmd_list[2]
                idx = int(cmd_list[-1]) - 1 if cmd_list[-1].isdigit() else 0

                if op == "SUB":
                    value = -value

                if axis == "COL":
                    if op == "MULTIPLY":
                        grid_array[:, idx] = grid_array[:, idx] * value
                    else:
                        grid_array[:, idx] = grid_array[:, idx] + value

                elif axis == "ROW":
                    if op == "MULTIPLY":
                        grid_array[idx] = grid_array[idx] * value
                    else:
                        grid_array[idx] = grid_array[idx] + value

                elif axis == "ALL":
                    if op == "MULTIPLY":
                        grid_array = grid_array * value
                    else:
                        grid_array = grid_array + value

            new_grid = []
            for row_data in grid_array:
                new_row = []
                for num in row_data:
                    while num > 1073741823:
                        num -= 1073741824
                    while num < 0:
                        num += 1073741824
                    new_row.append(num)
                new_grid.append(new_row)
            grid_array = np.array(new_grid)

        return grid_array

    def perform_control_actions(self, control_actions: list[str]):
        grid = self.grid_array.copy()
        instruc_list = self.instructions.copy()
        taken_actions = []
        for action in control_actions:
            if action == "TAKE":
                if instruc_list:
                    taken_actions = [instruc_list.pop(0)]
            elif action == "CYCLE":
                if taken_actions:
                    instruc_list.append(taken_actions.pop())
            elif action == "ACT":
                if taken_actions:
                    grid = self.perform_instructions(taken_actions, grid)
                    taken_actions = []
        return grid

    def perform_all_actions(self, control_actions: list[str]):
        grid = self.grid_array.copy()
        instruc_list = self.instructions.copy()
        taken_actions = []
        action_idx = 0
        while instruc_list or taken_actions:
            action = control_actions[action_idx]
            if action == "TAKE":
                if instruc_list:
                    taken_actions = [instruc_list.pop(0)]
            elif action == "CYCLE":
                if taken_actions:
                    instruc_list.append(taken_actions.pop())
            elif action == "ACT":
                if taken_actions:
                    grid = self.perform_instructions(taken_actions, grid)
                    taken_actions = []
            action_idx = (action_idx + 1) % len(control_actions)
        return grid

monster = CharybdisWhirlpool(num_grid, instructions)

grid_p1 = monster.perform_instructions(instructions, num_grid)
maxsum_p1 = monster.calculate_property_sum(grid_p1)
print("Part 1:", maxsum_p1)

grid_p2 = monster.perform_control_actions(control_actions)
maxsum_p2 = monster.calculate_property_sum(grid_p2)
print("Part 2:", maxsum_p2)

grid_p3 = monster.perform_all_actions(control_actions)
maxsum_p3 = monster.calculate_property_sum(grid_p3)
print("Part 3:", maxsum_p3)

